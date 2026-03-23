import pytest
import os
import asyncio
from unittest.mock import AsyncMock, patch
from pipecatapp.tools.autoresearch_tool import AutoresearchTool

def test_autoresearch_tool_run(tmp_path):
    target_file = tmp_path / "target.py"
    target_file.write_text("print('original')")

    # Create an LLM mock that returns failing code first, then passing code
    mock_llm = AsyncMock()
    mock_llm.generate.side_effect = [
        "<final_code>\nprint('first failed')\n</final_code>",
        "<final_code>\nprint('success')\n</final_code>"
    ]

    tool = AutoresearchTool(llm_client=mock_llm)

    def mock_eval(artifact, cmd, snapshot):
        if "first failed" in artifact.get("content", ""):
            return {"passed": False, "output": "fail"}
        return {"passed": True, "output": "pass"}

    with patch.object(tool, '_run_sandbox_eval', side_effect=mock_eval):
        result_json = asyncio.run(tool.run(
            target_file=str(target_file),
            test_command="python " + str(target_file),
            program_instructions="Fix the bug",
            max_iterations=2
        ))

        import json
        result = json.loads(result_json)

        assert result["total_iterations"] == 2
        assert result["code_changed"] == True

        # Check that it tried twice and succeeded on the second attempt
        history = result["history"]
        assert len(history) == 2
        assert history[0]["status"] == "reverted"
        assert history[1]["status"] == "committed"

        # Ensure the final file contains the successful code
        final_code = target_file.read_text()
        assert "print('success')" in final_code
