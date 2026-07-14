import pytest
import responses
import requests
from unittest.mock import patch, MagicMock
from pipecatapp.tools.last30days_tool import Last30DaysTool

def test_last30days_tool_initialization():
    tool = Last30DaysTool(service_url="http://localhost:8008", api_key="test-key")
    assert tool.name == "last30days"
    assert tool.service_url == "http://localhost:8008"
    assert tool.api_key == "test-key"

@responses.activate
def test_last30days_run_success():
    responses.add(
        responses.POST,
        "http://localhost:8008/research",
        json={"result": "Success compact brief from last30days-service"},
        status=200
    )

    tool = Last30DaysTool(service_url="http://localhost:8008", api_key="test-key")
    res = tool.run(topic="OpenAI", query_type="news", days=10, depth=1)

    assert res == "Success compact brief from last30days-service"
    assert len(responses.calls) == 1

    # Check payload parameters
    call_body = responses.calls[0].request.body.decode('utf-8')
    import json
    payload = json.loads(call_body)
    assert payload["topic"] == "OpenAI"
    assert payload["query_type"] == "news"
    assert payload["days"] == 10
    assert payload["depth"] == 1

@responses.activate
def test_last30days_run_failure():
    responses.add(
        responses.POST,
        "http://localhost:8008/research",
        body="Internal Server Error",
        status=500
    )

    tool = Last30DaysTool(service_url="http://localhost:8008", api_key="test-key")
    res = tool.run(topic="OpenAI")

    assert "Error: Failed to communicate" in res
