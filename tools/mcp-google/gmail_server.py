import os
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp-gmail")

PORT = int(os.getenv("MCP_GMAIL_PORT", "8083"))
GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", None)

class GmailHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "healthy", "service": "mcp-gmail", "mode": "live" if GMAIL_CREDENTIALS_PATH else "mock"})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            data = json.loads(body)
            action = data.get("action", "scan_leads")

            if action == "scan_leads":
                query = data.get("query", "label:leads subject:inquiry")
                mock_leads = [
                    {"id": "msg_001", "sender": "lead1@example.com", "subject": "Inquiry on cluster compute", "snippet": "Interested in deploying swarm containers..."},
                    {"id": "msg_002", "sender": "lead2@example.com", "subject": "Enterprise licensing", "snippet": "Would like to discuss Nomad integration details..."}
                ]
                self._send_json(200, {
                    "status": "ok",
                    "mode": "live" if GMAIL_CREDENTIALS_PATH else "mock",
                    "query": query,
                    "leads": mock_leads,
                    "count": len(mock_leads)
                })
            else:
                self._send_json(400, {"error": f"Unknown action: {action}"})

        except Exception as e:
            logger.error(f"Error handling Gmail request: {e}")
            self._send_json(500, {"error": str(e)})

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), GmailHandler)
    logger.info(f"MCP Gmail Server running on port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
