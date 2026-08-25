import os
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp-stripe")

PORT = int(os.getenv("MCP_STRIPE_PORT", "8082"))
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", None)

class StripeHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "healthy", "service": "mcp-stripe", "mode": "live" if STRIPE_API_KEY else "mock"})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            data = json.loads(body)
            action = data.get("action", "calculate_runway")

            if action == "calculate_runway":
                cash_balance = data.get("cash_balance", 100000.0)
                monthly_burn = data.get("monthly_burn", 15000.0)
                monthly_revenue = data.get("monthly_revenue", 5000.0)

                net_burn = monthly_burn - monthly_revenue
                runway_months = round(cash_balance / max(0.1, net_burn), 1) if net_burn > 0 else float("inf")

                self._send_json(200, {
                    "status": "ok",
                    "mode": "live" if STRIPE_API_KEY else "mock",
                    "cash_balance": cash_balance,
                    "net_burn": net_burn,
                    "runway_months": runway_months
                })

            elif action == "update_ledger":
                transaction_id = data.get("transaction_id", "tx_mock_123")
                amount = data.get("amount", 0.0)
                category = data.get("category", "general")

                logger.info(f"Ledger updated: {transaction_id} | Amount: {amount} | Category: {category}")
                self._send_json(200, {
                    "status": "ok",
                    "mode": "live" if STRIPE_API_KEY else "mock",
                    "transaction_id": transaction_id,
                    "updated": True
                })
            else:
                self._send_json(400, {"error": f"Unknown action: {action}"})

        except Exception as e:
            logger.error(f"Error processing request: {e}")
            self._send_json(500, {"error": str(e)})

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), StripeHandler)
    logger.info(f"MCP Stripe Server running on port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
