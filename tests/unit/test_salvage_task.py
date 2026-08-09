import sys
import os
import pytest

# Add scripts directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts')))

from salvage_task import synthesize_summary

def test_synthesize_summary_empty():
    assert synthesize_summary([], None) == "No completed steps found."
    assert synthesize_summary(None, {}) == "No completed steps found."

def test_synthesize_summary_standard_steps():
    completed_steps = [
        {"sequence": 1, "name": "step1", "return_value": "success"},
        {"sequence": 2, "name": "step2", "return_value": {"key": "value"}},
    ]
    summary = synthesize_summary(completed_steps, None)
    assert "### Executed Steps" in summary
    assert "- Step 1 (step1):" in summary
    assert "Result: success" in summary
    assert "- Step 2 (step2):" in summary
    assert "Result: {'key': 'value'}" in summary

def test_synthesize_summary_truncate_long_return_value():
    long_ret_val = "A" * 250
    completed_steps = [
        {"sequence": 1, "name": "step_long", "return_value": long_ret_val},
    ]
    summary = synthesize_summary(completed_steps, None)

    assert "Result: " + ("A" * 200) + "..." in summary
    # 200 As + "..." = 203 chars, plus "  Result: " prefix + \n suffix
    # So the total printed string is bounded
    assert len(summary) < 300

def test_synthesize_summary_with_context_messages():
    completed_steps = [{"sequence": 1, "name": "step1", "return_value": "done"}]
    last_context = {
        "messages": [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "world"},
        ]
    }
    summary = synthesize_summary(completed_steps, last_context)

    assert "### Final Conversation Context" in summary
    assert "- user: hello" in summary
    assert "- assistant: world" in summary

def test_synthesize_summary_truncate_long_message_content():
    completed_steps = [{"sequence": 1, "name": "step1", "return_value": "done"}]
    long_msg = "B" * 200
    last_context = {
        "messages": [
            {"role": "user", "content": long_msg},
        ]
    }
    summary = synthesize_summary(completed_steps, last_context)

    assert "- user: " + ("B" * 150) + "..." in summary

def test_synthesize_summary_slice_last_3_messages():
    completed_steps = [{"sequence": 1, "name": "step1", "return_value": "done"}]
    last_context = {
        "messages": [
            {"role": "user", "content": "msg1"},
            {"role": "assistant", "content": "msg2"},
            {"role": "user", "content": "msg3"},
            {"role": "assistant", "content": "msg4"},
            {"role": "user", "content": "msg5"},
        ]
    }
    summary = synthesize_summary(completed_steps, last_context)

    # msg1 and msg2 should be dropped
    assert "msg1" not in summary
    assert "msg2" not in summary

    # msg3, msg4, and msg5 should be included
    assert "msg3" in summary
    assert "msg4" in summary
    assert "msg5" in summary

def test_synthesize_summary_missing_message_keys():
    completed_steps = [{"sequence": 1, "name": "step1", "return_value": "done"}]
    last_context = {
        "messages": [
            # missing role
            {"content": "something"},
            # missing content
            {"role": "user"},
        ]
    }
    summary = synthesize_summary(completed_steps, last_context)

    assert "- unknown: something" in summary
    assert "- user: " in summary # content defaults to empty string
