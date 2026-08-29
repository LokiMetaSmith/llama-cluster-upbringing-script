import os
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp-docs")

PORT = int(os.getenv("MCP_DOCS_PORT", "8086"))
DOCS_CREDENTIALS_PATH = os.getenv("DOCS_CREDENTIALS_PATH", None)

class DocsHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "healthy", "service": "mcp-docs", "mode": "live" if DOCS_CREDENTIALS_PATH else "mock"})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            data = json.loads(body)
            action = data.get("action", "read_document")
            document_id = data.get("document_id", "mock_doc_abc")

            if action == "read_document":
                self._send_json(200, {
                    "status": "ok",
                    "mode": "live" if DOCS_CREDENTIALS_PATH else "mock",
                    "document_id": document_id,
                    "title": "Swarm Operations Architectural Guide",
                    "body": "This document specifies the agent swarm handoff procedures and evidence recording standards."
                })
            elif action == "append_text":
                text = data.get("text", "")
                self._send_json(200, {
                    "status": "ok",
                    "mode": "live" if DOCS_CREDENTIALS_PATH else "mock",
                    "document_id": document_id,
                    "appended_length": len(text)
                })
            else:
                self._send_json(400, {"error": f"Unknown action: {action}"})

        except Exception as e:
            logger.error(f"Error handling Docs request: {e}")
            self._send_json(500, {"error": str(e)})

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), DocsHandler)
    logger.info(f"MCP Docs Server running on port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
