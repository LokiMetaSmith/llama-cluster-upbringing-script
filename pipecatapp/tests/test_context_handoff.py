import pytest
from unittest.mock import patch, MagicMock
from pipecatapp.context_handoff import inject_context_handoff

def test_inject_context_handoff_adds_system_message():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"}
    ]

    with patch("pipecatapp.context_handoff.PolyphonyTool") as mock_polyphony_class:
        mock_instance = MagicMock()
        mock_polyphony_class.return_value = mock_instance

        updated_messages = inject_context_handoff(messages, "openrouter_claude_sonnet")

        # Verify PolyphonyTool called
        mock_instance.execute.assert_called_once_with("share", thought="Swarm Context Handoff triggered. Active model switched to: openrouter_claude_sonnet")

        # Verify length increased by 1 (system prompt added to front)
        assert len(updated_messages) == len(messages) + 1
        assert updated_messages[0]["role"] == "system"
        assert "openrouter_claude_sonnet" in updated_messages[0]["content"]
        assert updated_messages[1]["content"] == "Hello"
