import pytest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the parent directory and pipecatapp to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp')))

# Mock modules to allow clean imports
sys.modules["pyaudio"] = MagicMock()
sys.modules["faster_whisper"] = MagicMock()
sys.modules["piper"] = MagicMock()
sys.modules["piper.voice"] = MagicMock()
sys.modules["pipecat.transports.local.audio"] = MagicMock()

# Mock pipecat dependencies
mock_pipecat = MagicMock()
sys.modules["pipecat"] = mock_pipecat
sys.modules["pipecat.frames"] = mock_pipecat.frames
sys.modules["pipecat.frames.frames"] = mock_pipecat.frames.frames
sys.modules["pipecat.pipeline"] = mock_pipecat.pipeline
sys.modules["pipecat.pipeline.pipeline"] = mock_pipecat.pipeline.pipeline
sys.modules["pipecat.pipeline.runner"] = mock_pipecat.pipeline.runner
sys.modules["pipecat.pipeline.task"] = mock_pipecat.pipeline.task
sys.modules["pipecat.processors"] = mock_pipecat.processors
sys.modules["pipecat.processors.frame_processor"] = mock_pipecat.processors.frame_processor
sys.modules["pipecat.services"] = mock_pipecat.services
sys.modules["pipecat.services.openai"] = mock_pipecat.services.openai
sys.modules["pipecat.services.openai.llm"] = mock_pipecat.services.openai.llm

from pipecatapp.agent_factory import create_tools

@patch('pipecatapp.agent_factory.WOLTool')
@patch('pipecatapp.agent_factory.SaveSkillTool')
@patch('pipecatapp.agent_factory.SearchSkillsTool')
@patch('pipecatapp.agent_factory.Last30DaysTool')
@patch('pipecatapp.agent_factory.SSH_Tool')
@patch('pipecatapp.agent_factory.DesktopControlTool')
@patch('pipecatapp.agent_factory.CodeRunnerTool')
@patch('pipecatapp.agent_factory.WebBrowserTool')
@patch('pipecatapp.agent_factory.Ansible_Tool')
@patch('pipecatapp.agent_factory.Power_Tool')
@patch('pipecatapp.agent_factory.TermEverythingTool')
@patch('pipecatapp.agent_factory.RAG_Tool')
@patch('pipecatapp.agent_factory.HA_Tool')
@patch('pipecatapp.agent_factory.Git_Tool')
@patch('pipecatapp.agent_factory.OrchestratorTool')
@patch('pipecatapp.agent_factory.OpenClawTool')
@patch('pipecatapp.agent_factory.ATProtoTool')
@patch('pipecatapp.agent_factory.WasmTool')
@patch('pipecatapp.agent_factory.HereticTool')
@patch('pipecatapp.agent_factory.JulesTool')
@patch('pipecatapp.agent_factory.OCRTool')
@patch('pipecatapp.agent_factory.OpenWorkersTool')
@patch('pipecatapp.agent_factory.P2PSyncTool')
@patch('pipecatapp.agent_factory.SpecLoaderTool')
@patch('pipecatapp.agent_factory.SkillBuilderTool')
@patch('pipecatapp.agent_factory.FrugalSandboxTool')
@patch('pipecatapp.agent_factory.SchedulerTool')
@patch('pipecatapp.agent_factory.FieldGuideTool')
@patch('pipecatapp.agent_factory.DesignDocsTool')
def test_create_tools_instantiates_last30days(
        mock_design_docs, mock_field_guide, mock_scheduler,
    mock_frugal_sandbox, mock_skill_builder, mock_spec, mock_sync, mock_openworkers,
    mock_ocr, mock_jules, mock_heretic, mock_wasm, mock_atproto, mock_openclaw,
    mock_orchestrator, mock_git, mock_ha, mock_rag, mock_term, mock_power, mock_ansible,
    mock_web, mock_code, mock_desktop, mock_ssh, mock_last30days, mock_search,
    mock_save, mock_wol
):
    config = {
        "tool_execution_mode": "local",
        "last30days_service_url": "http://last30days-service.service.consul:8008",
        "tool_server_api_key": "some-key",
        "document_backend": {"type": "local", "directory": "/tmp"}
    }

    tools = create_tools(config)

    assert "last30days" in tools
    mock_last30days.assert_called_once_with(
        service_url="http://last30days-service.service.consul:8008",
        api_key="some-key"
    )
