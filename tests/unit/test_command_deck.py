import json
import pytest
import threading
import urllib.request
from http.server import HTTPServer
from command_deck.backend.app import CommandDeckAPIHandler, parse_models


def test_parse_models():
    """Verifies that models are correctly parsed and categorized into resource tiers."""
    models = parse_models()
    assert isinstance(models, dict)
    assert "edge_mid" in models
    assert "core" in models

    # Check structure of the parsed models list
    for tier in ["edge_mid", "core"]:
        for model in models[tier]:
            assert "name" in model
            assert "category" in model
            assert "memory_mb" in model
            assert "memory_gb" in model
            assert isinstance(model["memory_mb"], int)
            assert isinstance(model["memory_gb"], (int, float))


def test_api_server_endpoints():
    """Spins up the CommandDeck backend server on an ephemeral port and tests real-world HTTP requests."""
    # Start on port 0 to bind to any free available port
    server = HTTPServer(('127.0.0.1', 0), CommandDeckAPIHandler)
    port = server.server_address[1]

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        # 1. Test GET /api/models
        url_models = f"http://127.0.0.1:{port}/api/models"
        with urllib.request.urlopen(url_models) as response:
            assert response.status == 200
            assert "application/json" in response.headers.get("Content-Type", "")
            data = json.loads(response.read().decode('utf-8'))
            assert "edge_mid" in data
            assert "core" in data

        # 2. Test GET /api/status
        url_status = f"http://127.0.0.1:{port}/api/status"
        with urllib.request.urlopen(url_status) as response:
            assert response.status == 200
            assert "application/json" in response.headers.get("Content-Type", "")
            data = json.loads(response.read().decode('utf-8'))
            assert "status" in data
            assert data["status"] in ["idle", "running", "finished", "error"]
            assert "log_count" in data

        # 3. Test GET /index.html (static file serving)
        url_index = f"http://127.0.0.1:{port}/index.html"
        with urllib.request.urlopen(url_index) as response:
            assert response.status == 200
            assert "text/html" in response.headers.get("Content-Type", "")
            html_content = response.read().decode('utf-8')
            assert "COMMANDDECK" in html_content
            assert "system-status-text" in html_content

    finally:
        # Shutdown server gracefully
        server.shutdown()
        server.server_close()
        server_thread.join()
