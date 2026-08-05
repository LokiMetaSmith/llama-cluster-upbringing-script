import asyncio
import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Depends
import uvicorn
import aiomqtt
from pydantic import ValidationError

from config import settings
from models import DesfireEvent, TapResponse
from deduplicator import deduplicator
from authentik import authentik_client
from orchestrator import cluster_orchestrator

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
    while True:
        try:
            logger.info(f"Connecting to MQTT broker at {settings.mqtt_broker_host}:{settings.mqtt_broker_port}")
            async with aiomqtt.Client(hostname=settings.mqtt_broker_host, port=settings.mqtt_broker_port) as client:
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.tap_orchestrator_port)
