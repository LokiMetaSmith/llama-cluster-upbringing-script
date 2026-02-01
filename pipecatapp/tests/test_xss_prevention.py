from fastapi.testclient import TestClient
from web_server import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

@patch("web_server.WorkflowHistory")
def test_workflow_history_xss(mock_history_cls):
    """Test that workflow history endpoint escapes HTML in workflow names and status."""
    mock_history = MagicMock()
    mock_history_cls.return_value = mock_history

    # Simulate malicious data
    mock_history.get_all_runs.return_value = [
        {
            "id": "run1",
            "workflow_name": "<script>alert('XSS')</script>.yaml",
            "status": "failed<img src=x onerror=alert(1)>",
            "start_time": 1234567890
        }
    ]

    response = client.get("/api/workflows/history")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    run = data[0]

    # Verify escaping
    assert run["workflow_name"] == "&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;.yaml"
    assert run["status"] == "failed&lt;img src=x onerror=alert(1)&gt;"
