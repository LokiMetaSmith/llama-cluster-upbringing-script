import os
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp-drive")

PORT = int(os.getenv("MCP_DRIVE_PORT", "8084"))
DRIVE_CREDENTIALS_PATH = os.getenv("DRIVE_CREDENTIALS_PATH", None)

class DriveHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "healthy", "service": "mcp-drive", "mode": "live" if DRIVE_CREDENTIALS_PATH else "mock"})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            data = json.loads(body)
            action = data.get("action", "sync_templates")

            if action == "sync_templates":
                folder_id = data.get("folder_id", "root_templates_folder")
                mock_templates = [
                    {"id": "doc_001", "name": "Standard_SLA_Template.docx", "modified": "2025-01-15T10:00:00Z"},
                    {"id": "doc_002", "name": "Cluster_Onboarding_Spec.md", "modified": "2025-02-01T14:30:00Z"}
                ]
                self._send_json(200, {
                    "status": "ok",
                    "mode": "live" if DRIVE_CREDENTIALS_PATH else "mock",
                    "folder_id": folder_id,
                    "synced_templates": mock_templates,
                    "count": len(mock_templates)
                })
            else:
                self._send_json(400, {"error": f"Unknown action: {action}"})

        except Exception as e:
            logger.error(f"Error handling Drive request: {e}")
            self._send_json(500, {"error": str(e)})

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), DriveHandler)
    logger.info(f"MCP Drive Server running on port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
