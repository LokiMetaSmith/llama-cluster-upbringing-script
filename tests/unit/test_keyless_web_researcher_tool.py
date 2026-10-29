import pytest
from unittest.mock import patch, MagicMock
from pipecatapp.tools.keyless_web_researcher_tool import KeylessWebResearcherTool
import json

@pytest.fixture
def web_tool():
    return KeylessWebResearcherTool()

def test_get_schema(web_tool):
    schema = web_tool.get_schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "keyless_web_researcher"
    assert "action" in schema["function"]["parameters"]["properties"]
    assert "query" in schema["function"]["parameters"]["properties"]

@patch('pipecatapp.tools.keyless_web_researcher_tool.DDGS')
def test_search_text(mock_ddgs, web_tool):
    mock_instance = MagicMock()
    mock_ddgs.return_value.__enter__.return_value = mock_instance
    mock_instance.text.return_value = [
        {"title": "Test Title", "href": "https://test.com", "body": "Test body"}
    ]

    result = web_tool.execute("search_text", query="test query")
    assert "Test Title" in result
    assert "https://test.com" in result
    assert "Test body" in result

@patch('pipecatapp.tools.keyless_web_researcher_tool.DDGS')
def test_search_news(mock_ddgs, web_tool):
    mock_instance = MagicMock()
    mock_ddgs.return_value.__enter__.return_value = mock_instance
    mock_instance.news.return_value = [
        {"title": "News Title", "url": "https://news.com", "body": "News body"}
    ]

    result = web_tool.execute("search_news", query="news query")
    assert "News Title" in result
    assert "https://news.com" in result
    assert "News body" in result

@patch('pipecatapp.tools.keyless_web_researcher_tool.DDGS')
def test_search_no_results(mock_ddgs, web_tool):
    mock_instance = MagicMock()
    mock_ddgs.return_value.__enter__.return_value = mock_instance
    mock_instance.text.return_value = []

    result = web_tool.execute("search_text", query="no results")
    assert "No results found" in result

def test_invalid_action(web_tool):
    result = web_tool.execute("invalid_action", query="test")
    assert "Unknown action" in result
