import asyncio
import json
import logging
import os
import re
from datetime import datetime
import asyncio.streams
import paho.mqtt.client as mqtt
from pyod.models.iforest import IForest
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Constants
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt.service.consul")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
TCP_LISTEN_PORT = int(os.getenv("TCP_LISTEN_PORT", "9000"))

# State for PyOD anomaly detection (log volume over time windows)
# This is a very lightweight statistical check.
log_volumes = []
current_window_volume = 0
iforest_model = None
MODEL_TRAIN_THRESHOLD = 50 # Start predicting after 50 windows

def setup_mqtt():
    client = mqtt.Client(client_id="security_agent")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
            # Subscribe to agent communication channels for monitoring
            client.subscribe("cluster/messages/#")
            client.subscribe("cluster/agent/#")
        else:
            logger.error(f"Failed to connect to MQTT, return code {rc}")

    def on_message(client, userdata, msg):
        try:
            payload = msg.payload.decode('utf-8')
            if "malicious_payload_signature" in payload or "exec(" in payload:
                publish_alert(client, "high", f"Suspicious MQTT payload detected on {msg.topic}", {"payload": payload[:100]})
        except Exception as e:
            pass

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        return client
    except Exception as e:
        logger.error(f"Could not connect to MQTT: {e}")
        return None

def publish_alert(mqtt_client, severity, message, context=None):
    if not mqtt_client:
        return

    topic = f"cluster/security/alerts/{severity}"
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "severity": severity,
        "message": message,
        "context": context or {}
    }

    try:
        mqtt_client.publish(topic, json.dumps(payload))
        logger.info(f"Published alert to {topic}: {message}")
    except Exception as e:
        logger.error(f"Failed to publish alert: {e}")

async def process_log_line(line, mqtt_client):
    global current_window_volume
    current_window_volume += 1

    try:
        data = json.loads(line)
        message = str(data.get("message", "")).lower()

        # Rule 1: Failed SSH logins
        if "authentication failure" in message or "failed password" in message:
            publish_alert(mqtt_client, "low", "Failed authentication attempt detected.", data)

        # Rule 2: Nomad/Consul unauthorized access
        elif "permission denied" in message or "unauthorized" in message:
            publish_alert(mqtt_client, "high", "Unauthorized access attempt to cluster service.", data)

    except json.JSONDecodeError:
        # Not JSON, just process as raw string
        pass

async def statistical_monitoring_task(mqtt_client):
    global log_volumes, current_window_volume, iforest_model

    while True:
        await asyncio.sleep(60) # 1-minute windows

        # Record volume
        log_volumes.append([current_window_volume])
        logger.info(f"Log volume for past minute: {current_window_volume}")
        current_window_volume = 0

        # Keep history bounded
        if len(log_volumes) > 1000:
            log_volumes = log_volumes[-1000:]

        # Train/Predict
        if len(log_volumes) >= MODEL_TRAIN_THRESHOLD:
            try:
                X = np.array(log_volumes)
                if not iforest_model:
                    iforest_model = IForest(contamination=0.05, n_estimators=50) # Lightweight

                # Fit every 10 ticks to keep it light
                if len(log_volumes) % 10 == 0:
                    iforest_model.fit(X)

                # Predict the last window
                try:
                    # check if fitted without relying on internal attributes
                    is_anomaly = iforest_model.predict(X[-1].reshape(1, -1))[0]
                    if is_anomaly == 1:
                        publish_alert(mqtt_client, "low", "Anomalous log volume detected (statistical spike/drop).", {"volume": int(X[-1][0])})
                except Exception as e:
                    # Not fitted yet
                    pass
            except Exception as e:
                logger.error(f"PyOD anomaly detection error: {e}")

async def handle_client(reader, writer, mqtt_client):
    addr = writer.get_extra_info('peername')
    logger.info(f"Accepted log connection from {addr}")

    try:
        while True:
            data = await reader.readline()
            if not data:
                break

            line = data.decode('utf-8').strip()
            if line:
                await process_log_line(line, mqtt_client)
    except ConnectionResetError:
        pass
    except Exception as e:
        logger.error(f"Error handling TCP client {addr}: {e}")
    finally:
        logger.info(f"Connection from {addr} closed.")
        writer.close()
        await writer.wait_closed()

async def heartbeat_task(mqtt_client):
    while True:
        if mqtt_client:
            topic = "cluster/security/heartbeat"
            payload = {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "ok"
            }
            try:
                mqtt_client.publish(topic, json.dumps(payload))
            except Exception as e:
                logger.error(f"Failed to publish heartbeat: {e}")
        await asyncio.sleep(30)

async def main():
    logger.info("Starting Lightweight Security Agent...")

    mqtt_client = setup_mqtt()

    # Start the statistical monitoring background task
    asyncio.create_task(statistical_monitoring_task(mqtt_client))

    # Start heartbeat task
    asyncio.create_task(heartbeat_task(mqtt_client))

    # Start TCP Server for incoming logs (from Vector)
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, mqtt_client),
        '0.0.0.0', TCP_LISTEN_PORT
    )

    addr = server.sockets[0].getsockname()
    logger.info(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
