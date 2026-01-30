import asyncio
import json
import logging
import time
import uuid
from typing import Optional, Dict, Any

import websockets

logger = logging.getLogger(__name__)

class OpenClawClient:
    def __init__(self, gateway_url: str):
        self.gateway_url = gateway_url
        self.websocket = None
        self.device_id = str(uuid.uuid4())
        self._response_futures: Dict[str, asyncio.Future] = {}
        self._connected = False
        self._handshake_complete = asyncio.Event()

    async def connect(self):
        if self._connected and self.websocket:
            return

        logger.info(f"Connecting to OpenClaw Gateway at {self.gateway_url}")
        try:
            self.websocket = await websockets.connect(self.gateway_url)
            self._connected = True
            self._handshake_complete.clear()

            # Start listener loop in background
            asyncio.create_task(self._listen())

            # Wait for handshake to complete (challenge -> connect -> hello-ok)
            try:
                await asyncio.wait_for(self._handshake_complete.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                logger.error("OpenClaw handshake timed out")
                await self.disconnect()
                raise ConnectionError("OpenClaw handshake timed out")

        except Exception as e:
            logger.error(f"Failed to connect to OpenClaw: {e}")
            self._connected = False
            raise

    async def disconnect(self):
        if self.websocket:
            try:
                await self.websocket.close()
            except Exception:
                pass
        self.websocket = None
        self._connected = False

    async def _listen(self):
        try:
            async for message in self.websocket:
                await self._handle_message(message)
        except Exception as e:
            logger.error(f"OpenClaw WebSocket error: {e}")
        finally:
            self._connected = False

    async def _handle_message(self, message: str):
        try:
            data = json.loads(message)
            msg_type = data.get("type")

            if msg_type == "event":
                event_name = data.get("event")
                if event_name == "connect.challenge":
                    await self._handle_challenge(data.get("payload"))

            elif msg_type == "res":
                # Handle responses to requests
                req_id = data.get("id")

                # Check for hello-ok payload in response which might complete handshake
                payload = data.get("payload", {})
                if isinstance(payload, dict) and payload.get("type") == "hello-ok":
                    self._handshake_complete.set()

                if req_id in self._response_futures:
                    future = self._response_futures.pop(req_id)
                    if not future.done():
                        future.set_result(data)

        except Exception as e:
            logger.error(f"Error handling OpenClaw message: {e}")

    async def _handle_challenge(self, payload: Dict[str, Any]):
        # Received challenge, send connect request
        connect_req = {
            "type": "req",
            "id": str(uuid.uuid4()),
            "method": "connect",
            "params": {
                "minProtocol": 3,
                "maxProtocol": 3,
                "client": {
                    "id": "pipecat-agent",
                    "version": "1.0.0",
                    "platform": "linux",
                    "mode": "operator"
                },
                "role": "operator",
                "scopes": ["operator.write"],
                "caps": [],
                "commands": [],
                "permissions": {},
                "auth": {
                    "token": "" # Empty for local/auto-approve
                },
                "locale": "en-US",
                "userAgent": "pipecat-agent/1.0.0",
                "device": {
                    "id": self.device_id,
                    "publicKey": "", # Omitted for unsigned
                    "signature": "",
                    "signedAt": int(time.time() * 1000),
                    "nonce": payload.get("nonce")
                }
            }
        }
        await self._send_json(connect_req)

    async def _send_json(self, data: Dict[str, Any]):
        if self.websocket:
            await self.websocket.send(json.dumps(data))

    async def send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if not self._connected:
            await self.connect()

        req_id = str(uuid.uuid4())
        req = {
            "type": "req",
            "id": req_id,
            "method": method,
            "params": params
        }

        future = asyncio.get_running_loop().create_future()
        self._response_futures[req_id] = future

        await self._send_json(req)

        try:
            response = await asyncio.wait_for(future, timeout=10.0)
            if not response.get("ok"):
                raise Exception(f"OpenClaw error: {response.get('payload', response)}")
            return response
        except asyncio.TimeoutError:
            if req_id in self._response_futures:
                del self._response_futures[req_id]
            raise TimeoutError(f"Request {method} timed out")

    async def send_message(self, target: str, message: str, channel: Optional[str] = None):
        params = {
            "target": target,
            "message": message
        }
        if channel:
            params["channel"] = channel

        return await self.send_request("message.send", params)
