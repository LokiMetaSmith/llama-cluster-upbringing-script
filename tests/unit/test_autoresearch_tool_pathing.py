import pytest
import os
import asyncio
from unittest.mock import AsyncMock, patch
from pipecatapp.tools.autoresearch_tool import AutoresearchTool
import tempfile

def test_autoresearch_tool_pathing(tmp_path):
    target_file = tmp_path / "target.py"
    target_file.write_text("print('original')")

    # Create an LLM mock
    mock_llm = AsyncMock()
    mock_llm.generate.return_value = "<final_code>\nprint('success')\n</final_code>"

    tool = AutoresearchTool(llm_client=mock_llm)

    def mock_eval(artifact, cmd, snapshot):
        # We assert that the artifact path passed to sandbox eval is relative
        # or properly normalized, not an absolute system path that would break the sandbox
        assert not os.path.isabs(artifact["file_path"]), f"Expected relative path, got {artifact['file_path']}"
        return {"passed": True, "output": "pass"}

    with patch.object(tool, '_run_sandbox_eval', side_effect=mock_eval):
        # Pass an absolute path
        abs_target_file = str(target_file.absolute())

        result_json = asyncio.run(tool.run(
            target_file=abs_target_file,
            test_command="python " + abs_target_file,
            program_instructions="Fix the bug",
            max_iterations=1
        ))

        import json
        result = json.loads(result_json)
        assert result["code_changed"] == True
