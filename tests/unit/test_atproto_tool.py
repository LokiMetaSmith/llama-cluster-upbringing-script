import pytest
import asyncio
from unittest.mock import MagicMock, patch
from pipecatapp.tools.atproto_tool import ATProtoTool

def test_atproto_tool_initialization():
    tool = ATProtoTool("user", "pass", buffer_db_path=":memory:")
    assert tool.name == "atproto"
    assert tool.username == "user"

def test_send_post_queues_locally():
    # Since we are using an async tool context, we don't start the worker loop explicitly for the sync test
    tool = ATProtoTool("user", "pass", buffer_db_path=":memory:")

    res = asyncio.run(tool.send_post("Hello World offline"))
    assert "Post queued successfully" in res

    # Check that it is actually in the buffer
    pending = tool.buffer.get_pending_events()
    assert len(pending) == 1
    assert pending[0]['action'] == 'send_post'
    assert pending[0]['payload']['text'] == 'Hello World offline'

def test_get_timeline_offline():
    tool = ATProtoTool("user", "pass", buffer_db_path=":memory:")

    # Mock getting client to throw an exception to simulate offline
    with patch("pipecatapp.tools.atproto_tool.ATProtoTool._get_client", side_effect=Exception("Network unreachable")):
        res = asyncio.run(tool.get_timeline())
        assert "Could not fetch timeline" in res
        assert "Network unreachable" in res

def test_get_timeline_online():
    tool = ATProtoTool("user", "pass", buffer_db_path=":memory:")

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
