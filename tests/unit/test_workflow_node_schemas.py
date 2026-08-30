import pytest
from fastapi.testclient import TestClient
from pipecatapp.web_server import app
from pipecatapp.api_keys import get_api_key

def test_workflow_node_schemas_endpoint():
    app.dependency_overrides[get_api_key] = lambda: "test_key"
    try:
        client = TestClient(app)
        response = client.get("/api/workflows/node_schemas")

        assert response.status_code == 200
        data = response.json()

        assert "schemas" in data
        assert "nodes" in data

        schemas = data["schemas"]

        # Verify custom nodes are present
        assert "ComplexityEvaluatorNode" in schemas
        assert "ComfyUIBridgeNode" in schemas
        assert "CircuitBreakerNode" in schemas
        assert "HITLGateNode" in schemas

        # Check schema properties for ComfyUIBridgeNode
        comfy_schema = schemas["ComfyUIBridgeNode"]
        assert comfy_schema["category"] == "Visual AI & VR"
        assert "expected_inputs" in comfy_schema
        assert "expected_outputs" in comfy_schema
    finally:
        app.dependency_overrides.clear()
