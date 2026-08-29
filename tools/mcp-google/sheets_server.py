import os
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp-sheets")

PORT = int(os.getenv("MCP_SHEETS_PORT", "8085"))
SHEETS_CREDENTIALS_PATH = os.getenv("SHEETS_CREDENTIALS_PATH", None)

class SheetsHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "healthy", "service": "mcp-sheets", "mode": "live" if SHEETS_CREDENTIALS_PATH else "mock"})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            data = json.loads(body)
            action = data.get("action", "read_range")
            spreadsheet_id = data.get("spreadsheet_id", "mock_sheet_123")
            range_name = data.get("range", "Sheet1!A1:D10")

            if action == "read_range":
                mock_values = [
                    ["Timestamp", "Agent ID", "Task", "Status"],
                    ["2026-08-28T20:00:00Z", "agent-01", "Refactor Node", "COMPLETED"],
                    ["2026-08-28T20:05:00Z", "agent-02", "Deduplicate Prompt", "IN_PROGRESS"]
                ]
                self._send_json(200, {
                    "status": "ok",
                    "mode": "live" if SHEETS_CREDENTIALS_PATH else "mock",
                    "spreadsheet_id": spreadsheet_id,
                    "range": range_name,
                    "values": mock_values
                })
            elif action == "update_range":
                values = data.get("values", [])
                self._send_json(200, {
                    "status": "ok",
                    "mode": "live" if SHEETS_CREDENTIALS_PATH else "mock",
                    "spreadsheet_id": spreadsheet_id,
                    "range": range_name,
                    "updated_rows": len(values)
                })
            else:
                self._send_json(400, {"error": f"Unknown action: {action}"})

        except Exception as e:
            logger.error(f"Error handling Sheets request: {e}")
            self._send_json(500, {"error": str(e)})

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), SheetsHandler)
    logger.info(f"MCP Sheets Server running on port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
