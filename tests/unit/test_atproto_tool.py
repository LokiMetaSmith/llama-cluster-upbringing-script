import pytest
import asyncio
from unittest.mock import MagicMock, patch
from pipecatapp.tools.atproto_tool import ATProtoTool

def test_atproto_tool_initialization():
    tool = ATProtoTool("user", "pass")
    assert tool.name == "atproto"
    assert tool.username == "user"

def test_send_post():
    tool = ATProtoTool("user", "pass")

    mock_client = MagicMock()
    mock_client.send_post.return_value = MagicMock(uri="at://mock/uri")

    with patch("pipecatapp.tools.atproto_tool.ATProtoTool._get_client", return_value=mock_client):
        res = asyncio.run(tool.send_post("Hello World"))
        assert "Post sent successfully" in res
        assert "at://mock/uri" in res

def test_get_timeline():
    tool = ATProtoTool("user", "pass")

    mock_client = MagicMock()
    mock_post1 = MagicMock()
    mock_post1.post.author.handle = "alice"
    mock_post1.post.record.text = "Hello"

    mock_post2 = MagicMock()
    mock_post2.post.author.handle = "bob"
    # No text attribute
    del mock_post2.post.record.text

    mock_timeline = MagicMock()
    mock_timeline.feed = [mock_post1, mock_post2]
    mock_client.get_timeline.return_value = mock_timeline

    with patch("pipecatapp.tools.atproto_tool.ATProtoTool._get_client", return_value=mock_client):
        res = asyncio.run(tool.get_timeline())
        assert "@alice: Hello" in res
        assert "@bob: [No Text/Media Only]" in res
