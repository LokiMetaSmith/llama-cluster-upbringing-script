import asyncio
import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Depends
import uvicorn
import ssl
import aiomqtt
from pydantic import ValidationError

from services.tap_orchestrator.config import settings

import time
import secrets
from services.tap_orchestrator.models import DesfireEvent, TapResponse, ChallengeResponse, VerifyRequest, VerifyResponse
from pipecatapp.atproto_crypto import verify_payload
from pipecatapp.datalog_memory import DatalogMemory
from pipecatapp.memory_backends_impl.consul_kv_backend import ConsulKVBackend

# Datalog & Consul initialization for REA Accounting
datalog = DatalogMemory()
consul_backend = ConsulKVBackend(prefix="swarm/")

# Temporary store for nonces (nonce -> expiration_time)
challenge_store = {}
NONCE_TTL = 10  # seconds

from services.tap_orchestrator.deduplicator import deduplicator
from services.tap_orchestrator.authentik import authentik_client
from services.tap_orchestrator.orchestrator import cluster_orchestrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("tap_orchestrator")

async def publish_mqtt_status(client: aiomqtt.Client, topic: str, status: str, message: str, user_id: str):
    """Publish a status message back to the MQTT broker."""
    payload = json.dumps({"status": status, "message": message, "user_id": user_id})
    try:
        await client.publish(topic, payload)
        logger.debug(f"Published status to {topic}: {payload}")
    except Exception as e:
        logger.error(f"Failed to publish status to {topic}: {e}")

async def process_tap_event(event: DesfireEvent, mqtt_client=None):
    """
    Main processing pipeline for a tap event.
    """
    if not deduplicator.is_allowed(event.user_id):
        logger.info(f"Duplicate tap ignored for user: {event.user_id}")
        return

    logger.info(f"Processing valid tap event for user: {event.user_id}")

    try:
        # 1. Authentik Identity Verification
        user = await authentik_client.get_user(event.user_id)

        if not user:
            logger.warning(f"Authentication failed: User {event.user_id} not found in Authentik")
            if mqtt_client:
                await publish_mqtt_status(mqtt_client, settings.mqtt_topic_failure, "error", "User not found", event.user_id)
            return

        if not user.is_active:
            logger.warning(f"Authentication failed: User {event.user_id} is disabled")
            if mqtt_client:
                await publish_mqtt_status(mqtt_client, settings.mqtt_topic_failure, "error", "User disabled", event.user_id)
            return

        logger.info(f"User {event.user_id} authenticated successfully. Groups: {user.groups}")

        # 2. Cluster Resource Hot-Loading
        await cluster_orchestrator.execute_hot_load(user)

        logger.info(f"Successfully processed tap event for {event.user_id}")

    except Exception as e:
        logger.error(f"Error in processing pipeline for {event.user_id}: {e}")
        if mqtt_client:
            await publish_mqtt_status(mqtt_client, settings.mqtt_topic_failure, "error", "Internal processing error", event.user_id)

async def mqtt_listener():
    """
    Background task to listen for MQTT tap events.
    """
    reconnect_interval = 5
    tls_context = None
    if settings.mqtt_ca_cert:
        tls_context = ssl.create_default_context(cafile=settings.mqtt_ca_cert)
        if settings.mqtt_client_cert and settings.mqtt_client_key:
            tls_context.load_cert_chain(certfile=settings.mqtt_client_cert, keyfile=settings.mqtt_client_key)
        # Check hostname might need to be bypassed if using IP address in cert
        tls_context.check_hostname = False

    while True:
        try:
            logger.info(f"Connecting to MQTT broker at {settings.mqtt_broker_host}:{settings.mqtt_broker_port}")
            async with aiomqtt.Client(hostname=settings.mqtt_broker_host, port=settings.mqtt_broker_port, tls_context=tls_context) as client:
                logger.info(f"Subscribing to {settings.mqtt_topic_success}")
                await client.subscribe(settings.mqtt_topic_success)
                async for message in client.messages:
                    try:
                        payload = message.payload.decode()
                        logger.debug(f"Received MQTT payload: {payload}")

                        data = json.loads(payload)
                        event = DesfireEvent(**data)

                        # Process the event without blocking the listener loop
                        asyncio.create_task(process_tap_event(event, mqtt_client=client))

                    except json.JSONDecodeError:
                        logger.error(f"Invalid JSON payload received: {payload}")
                    except ValidationError as e:
                        logger.error(f"Invalid event schema: {e}")
                    except Exception as e:
                        logger.error(f"Error processing MQTT message: {e}")
        except aiomqtt.MqttError as e:
            logger.error(f"MQTT connection error: {e}. Reconnecting in {reconnect_interval} seconds...")
            await asyncio.sleep(reconnect_interval)
        except asyncio.CancelledError:
            logger.info("MQTT listener cancelled")
            break
        except Exception as e:
            logger.error(f"Unexpected error in MQTT listener: {e}")
            await asyncio.sleep(reconnect_interval)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Tap Orchestrator service")
    mqtt_task = asyncio.create_task(mqtt_listener())
    yield
    # Shutdown
    logger.info("Shutting down Tap Orchestrator service")
    mqtt_task.cancel()
    await authentik_client.close()

app = FastAPI(title="Tap Orchestrator", lifespan=lifespan)

async def verify_secret(x_tap_secret: str = Header(...)):
    if x_tap_secret != settings.tap_orchestrator_secret:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_tap_secret

@app.post("/api/v1/tap-event", response_model=TapResponse)
async def handle_tap_webhook(event: DesfireEvent, secret: str = Depends(verify_secret)):
    """
    Fallback HTTP REST endpoint for tap events.
    """
    logger.info(f"Received tap event via HTTP webhook for user: {event.user_id}")

    # Process asynchronously to return acknowledgment quickly
    asyncio.create_task(process_tap_event(event))

    return TapResponse(status="success", message="Tap event queued for processing")


@app.get("/api/v1/challenge", response_model=ChallengeResponse)
async def get_challenge(room_id: str):
    """
    Generates an ephemeral, randomized cryptographic challenge for presence verification.
    """
    nonce = secrets.token_hex(16)
    expires_at = time.time() + NONCE_TTL
    challenge_store[nonce] = {
        "room_id": room_id,
        "expires_at": expires_at
    }

    # Cleanup expired nonces (lazy approach for prototype)
    expired = [k for k, v in challenge_store.items() if v["expires_at"] < time.time()]
    for k in expired:
        del challenge_store[k]

    return ChallengeResponse(
        nonce=nonce,
        room_id=room_id,
        expires_in=NONCE_TTL
    )

@app.post("/api/v1/verify", response_model=VerifyResponse)
async def verify_presence(request: VerifyRequest):
    """
    Verifies the device's signature of the challenge nonce and updates mutual credit.
    """
    now = time.time()

    # 1. Check if nonce is valid and unexpired
    if request.challenge_nonce not in challenge_store:
        raise HTTPException(status_code=400, detail="Invalid or expired challenge nonce")

    stored_challenge = challenge_store.pop(request.challenge_nonce)

    if stored_challenge["expires_at"] < now:
        raise HTTPException(status_code=400, detail="Challenge nonce expired")

    if stored_challenge["room_id"] != request.room_id:
        raise HTTPException(status_code=400, detail="Room ID mismatch")

    # 2. Verify Cryptographic Signature
    payload_to_verify = {
        "challenge_nonce": request.challenge_nonce,
        "room_id": request.room_id
    }
    if request.metadata:
        payload_to_verify["metadata"] = request.metadata

    is_valid = verify_payload(payload_to_verify, request.signature, request.public_key_hex)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid signature")

    # 3. Account: Log event to REA / Datalog
    datalog.assert_fact("presence", request.did, request.room_id, now)

    # 4. Allocate: Calculate compute weight and write to Consul
    # The default get_available_credit uses `agent_id`, which we map to `did`
    try:
        weight = datalog.engine.get_available_credit(request.did)
    except Exception as e:
        logger.error(f"Failed to calculate credit for {request.did}: {e}")
        weight = 0.0

    try:
        consul_backend.put_kv(f"compute_rights/{request.did}", {"weight": weight, "room_id": request.room_id, "last_verified": now})
    except Exception as e:
        logger.error(f"Failed to write compute weight to Consul: {e}")

    return VerifyResponse(
        status="success",
        message="Presence verified and compute weight allocated.",
        weight=weight
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.tap_orchestrator_port)
