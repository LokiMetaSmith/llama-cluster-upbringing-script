import sys
import os
import types

# Ensure /opt and repo paths are discoverable across standalone and repository runs
for p in ["/opt", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))]:
    if p and os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

if "services" not in sys.modules:
    sys.modules["services"] = types.ModuleType("services")
if "services.tap_orchestrator" not in sys.modules:
    try:
        import tap_orchestrator
        sys.modules["services.tap_orchestrator"] = tap_orchestrator
    except ImportError:
        pass

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
from services.tap_orchestrator.models import (
    DesfireEvent,
    TapResponse,
    ChallengeResponse,
    VerifyRequest,
    VerifyResponse,
    RFTelemetryFrame,
    RFPresenceResponse,
    ClusterSession,
    SessionCreateRequest,
    SessionStatusResponse,
    SessionRevokeRequest,
)
from pipecatapp.atproto_crypto import verify_payload
from pipecatapp.datalog_memory import DatalogMemory
from pipecatapp.memory_backends_impl.consul_kv_backend import ConsulKVBackend
from services.tap_orchestrator.rf_sniffer import RFSnifferEngine

# Datalog & Consul initialization for REA Accounting
datalog = DatalogMemory()
consul_backend = ConsulKVBackend(prefix="swarm/")
rf_sniffer_engine = RFSnifferEngine(datalog=datalog, consul_backend=consul_backend)

# Temporary store for nonces (nonce -> expiration_time)
challenge_store = {}
NONCE_TTL = 10  # seconds

# Active session storage (user_id/did -> ClusterSession, token -> ClusterSession)
active_sessions: dict[str, ClusterSession] = {}
token_sessions: dict[str, ClusterSession] = {}

def create_or_update_session(
    user_id: str,
    did: str = None,
    auth_method: str = "fido2",
    ttl_seconds: int = 3600,
    roles: list = None,
    allowed_targets: list = None,
    public_key: str = None,
    public_keys: list = None,
    metadata: dict = None
) -> ClusterSession:
    now = time.time()
    session_id = f"sess_{secrets.token_hex(12)}"
    session_token = f"swarm_st_{secrets.token_urlsafe(24)}"

    if roles is None:
        roles = ["operator", "admin"] if user_id in ("admin", "operator", "loki") or "admin" in (did or "") else ["operator"]
    if allowed_targets is None:
        allowed_targets = ["terminal", "grafana", "nomad", "consul", "compute"]

    session = ClusterSession(
        session_id=session_id,
        session_token=session_token,
        user_id=user_id,
        did=did or user_id,
        auth_method=auth_method,
        roles=roles,
        allowed_targets=allowed_targets,
        created_at=now,
        expires_at=now + ttl_seconds,
        is_active=True,
        public_key=public_key,
        public_keys=public_keys,
        metadata=metadata or {}
    )

    active_sessions[user_id] = session
    token_sessions[session_token] = session
    if did:
        active_sessions[did] = session

    # Synchronize to Consul KV fast state
    try:
        session_dict = session.model_dump()
        consul_backend.put_kv(f"sessions/{user_id}", session_dict)
        consul_backend.put_kv(f"tokens/{session_token}", session_dict)
        if did and did != user_id:
            consul_backend.put_kv(f"sessions/{did}", session_dict)
    except Exception as e:
        logger.warning(f"Could not write session to Consul KV: {e}")

    logger.info(f"ClusterSession created for user {user_id} (method: {auth_method}, ttl: {ttl_seconds}s)")
    return session

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

        # 3. Create active ClusterSession in Consul KV
        session = create_or_update_session(
            user_id=user.username,
            auth_method="desfire_nfc",
            roles=user.groups or ["operator"],
            metadata={"reader_id": event.reader_id, "auth_type": event.auth_type}
        )

        logger.info(f"Successfully processed tap event and established session for {event.user_id}")

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

    # 5. Issue Active ClusterSession and publish to Consul KV
    session = create_or_update_session(
        user_id=request.did,
        did=request.did,
        auth_method="challenge_attestation",
        ttl_seconds=3600,
        public_key=request.public_key_hex,
        metadata={"room_id": request.room_id, **(request.metadata or {})}
    )

    return VerifyResponse(
        status="success",
        message="Presence verified and cluster session activated.",
        weight=weight,
        session=session,
        session_token=session.session_token
    )

@app.post("/api/v1/session/create", response_model=SessionStatusResponse)
async def create_session(request: SessionCreateRequest, x_tap_secret: str = Header(None)):
    """
    Explicitly creates an active cluster session for a validated user/DID.
    Protected by tap secret header or local trusted loopback.
    """
    if x_tap_secret and x_tap_secret != settings.tap_orchestrator_secret:
        raise HTTPException(status_code=403, detail="Invalid tap secret")

    session = create_or_update_session(
        user_id=request.user_id,
        did=request.did,
        auth_method=request.auth_method,
        ttl_seconds=request.ttl_seconds or 3600,
        roles=request.roles,
        allowed_targets=request.allowed_targets,
        public_key=request.public_key,
        public_keys=request.public_keys,
        metadata=request.metadata
    )

    remaining = max(0, int(session.expires_at - time.time()))
    return SessionStatusResponse(
        status="success",
        valid=True,
        remaining_seconds=remaining,
        session=session
    )

@app.get("/api/v1/session/status", response_model=SessionStatusResponse)
async def get_session_status(
    token: str = None,
    user_id: str = None,
    authorization: str = Header(None)
):
    """
    Verifies if an active, unexpired session exists for a user, DID, or session token.
    Used by terminals, PAM modules, SSH hooks, and reverse proxies.
    """
    now = time.time()
    search_token = token
    if not search_token and authorization and authorization.startswith("Bearer "):
        search_token = authorization[len("Bearer "):].strip()

    session = None
    if search_token:
        session = token_sessions.get(search_token)
        if not session:
            # Check Consul KV fallback
            data = consul_backend.get_kv(f"tokens/{search_token}")
            if data and isinstance(data, dict):
                session = ClusterSession(**data)
                token_sessions[search_token] = session

    if not session and user_id:
        session = active_sessions.get(user_id)
        if not session:
            # Check Consul KV fallback
            data = consul_backend.get_kv(f"sessions/{user_id}")
            if data and isinstance(data, dict):
                session = ClusterSession(**data)
                active_sessions[user_id] = session

    if not session:
        return SessionStatusResponse(status="not_found", valid=False, remaining_seconds=0, session=None)

    if not session.is_active or session.expires_at < now:
        return SessionStatusResponse(status="expired", valid=False, remaining_seconds=0, session=session)

    remaining = int(session.expires_at - now)
    return SessionStatusResponse(status="active", valid=True, remaining_seconds=remaining, session=session)

@app.post("/api/v1/session/revoke", response_model=SessionStatusResponse)
async def revoke_session(request: SessionRevokeRequest):
    """
    Immediately revokes an active session.
    """
    target_session = None
    if request.session_token and request.session_token in token_sessions:
        target_session = token_sessions.pop(request.session_token)
    elif request.user_id and request.user_id in active_sessions:
        target_session = active_sessions.pop(request.user_id)

    if target_session:
        target_session.is_active = False
        try:
            consul_backend.delete_kv(f"sessions/{target_session.user_id}")
            consul_backend.delete_kv(f"tokens/{target_session.session_token}")
            if target_session.did:
                consul_backend.delete_kv(f"sessions/{target_session.did}")
        except Exception as e:
            logger.warning(f"Could not purge session from Consul KV: {e}")

        return SessionStatusResponse(status="revoked", valid=False, remaining_seconds=0, session=target_session)

    return SessionStatusResponse(status="not_found", valid=False, remaining_seconds=0, session=None)

@app.post("/api/v1/telemetry/rf", response_model=RFPresenceResponse)
async def process_rf_telemetry(frame: RFTelemetryFrame):
    """
    Processes RF/Wi-Fi promiscuous/SDR signal telemetry for passive presence detection.
    """
    try:
        return rf_sniffer_engine.process_telemetry_frame(frame)
    except Exception as e:
        logger.error(f"Error processing RF telemetry frame: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process RF telemetry: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.tap_orchestrator_port)
