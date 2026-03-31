import pytest
from unittest.mock import patch, MagicMock
from pipecatapp.tools.heretic_tool import HereticTool

def test_heretic_tool_align_model():
    tool = HereticTool(root_dir="/tmp")

    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = "Heretic completed successfully"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = tool.align_model(
            model="test-model",
            harmful_dataset="harmful.json",
            harmless_dataset="harmless.json",
            reverse=True,
            output_dir="/tmp/output"
        )

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]

        assert "heretic" in args
        assert "test-model" in args
        assert "--harmful-dataset" in args
        assert "harmful.json" in args
        assert "--harmless-dataset" in args
        assert "harmless.json" in args
        assert "--reverse" in args
        assert "--save-path" in args
        assert "/tmp/output" in args

        assert result["returncode"] == 0
        assert "completed successfully" in result["stdout"]
