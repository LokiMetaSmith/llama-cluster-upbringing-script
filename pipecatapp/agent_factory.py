import os
from tools.ssh_tool import SSH_Tool
from tools.mcp_tool import MCP_Tool
from tools.desktop_control_tool import DesktopControlTool
from tools.code_runner_tool import CodeRunnerTool
from tools.web_browser_tool import WebBrowserTool
from tools.ansible_tool import Ansible_Tool
from tools.power_tool import Power_Tool
from tools.summarizer_tool import SummarizerTool
from tools.term_everything_tool import TermEverythingTool
from tools.rag_tool import RAG_Tool
from tools.ha_tool import HA_Tool
from tools.git_tool import Git_Tool
from tools.orchestrator_tool import OrchestratorTool
from tools.llxprt_code_tool import LLxprt_Code_Tool
from tools.claude_clone_tool import ClaudeCloneTool
from tools.smol_agent_tool import SmolAgentTool
from tools.final_answer_tool import FinalAnswerTool
from tools.shell_tool import ShellTool
from tools.prompt_improver_tool import PromptImproverTool
from tools.council_tool import CouncilTool
from tools.swarm_tool import SwarmTool
from tools.project_mapper_tool import ProjectMapperTool
from tools.planner_tool import PlannerTool
from tools.file_editor_tool import FileEditorTool
from tools.archivist_tool import ArchivistTool
from tools.opencode_tool import OpencodeTool
from tools.dependency_scanner_tool import DependencyScannerTool
from tools.remote_tool_proxy import RemoteToolProxy
from tools.vr_tool import VRTool
from tools.experiment_tool import ExperimentTool
from tools.submit_solution_tool import SubmitSolutionTool
from tools.container_registry_tool import ContainerRegistryTool
from tools.search_tool import SearchTool
from tools.openclaw_tool import OpenClawTool
from tools.mkv_tool import MKV_Tool
from tools.miniray_tool import MinirayTool
from tools.scheduler_tool import SchedulerTool
from tools.context_upload_tool import ContextUploadTool
from tools.personality_tool import PersonalityTool

# Tools that are supported by the Tool Server and can be proxied
REMOTE_SUPPORTED_TOOLS = [
    "ssh", "desktop_control", "code_runner", "web_browser",
    "ansible", "power", "term_everything", "rag", "ha",
    "git", "orchestrator"
]

def create_tools(config: dict, twin_service=None, runner=None) -> dict:
    """
    Initializes and returns the dictionary of tools.

    Args:
        config (dict): Configuration dictionary (e.g. from Consul).
        twin_service: Reference to the agent/service using the tools (optional).
        runner: Reference to the pipeline runner (optional).

    Returns:
        dict: A dictionary of tool instances.
    """

    mode = config.get("tool_execution_mode", "local")
    tool_server_url = config.get("tool_server_url")

    # Start with tools that are ALWAYS local (complex deps or not on tool server)
    tools = {
        "mcp": MCP_Tool(twin_service, runner) if twin_service and runner else None,
        "smol_agent_computer": SmolAgentTool(),
        "llxprt_code": LLxprt_Code_Tool(),
        "claude_clone": ClaudeCloneTool(),
        "final_answer": FinalAnswerTool(),
        "shell": ShellTool(),
        "prompt_improver": PromptImproverTool(twin_service) if twin_service else None,
        "council": CouncilTool(twin_service) if twin_service else None,
        "swarm": SwarmTool(),
        "project_mapper": ProjectMapperTool(),
        "planner": PlannerTool(twin_service) if twin_service else None,
        "file_editor": FileEditorTool(root_dir="/opt/pipecatapp"),
        "archivist": ArchivistTool(),
        "opencode": OpencodeTool(
            base_url=config.get("opencode_api_url"),
            provider_id=config.get("opencode_provider", "openai"),
            model_id=config.get("opencode_model", "gpt-4o")
        ),
        "dependency_scanner": DependencyScannerTool(),
        "vr": VRTool(),
        "experiment": ExperimentTool(),
        "submit_solution": SubmitSolutionTool(),
        "container_registry": ContainerRegistryTool(),
        "search": SearchTool(root_dir="/opt/pipecatapp"),
        "openclaw": OpenClawTool(
            gateway_url=config.get("openclaw_gateway_url", "ws://moltbot.service.consul:18789")
        ),
        "mkv_store": MKV_Tool(),
        "miniray_compute": MinirayTool(),
        "scheduler": SchedulerTool(),
        "context_upload": ContextUploadTool(),
        "personality": PersonalityTool(api_url=config.get("llama_api_url")),
    }

    # Inject memory client into SwarmTool if available (for Map-Reduce)
    if "swarm" in tools and twin_service and hasattr(twin_service, "long_term_memory"):
        tools["swarm"].memory_client = twin_service.long_term_memory

    if config.get("use_summarizer", False) and twin_service:
        tools["summarizer"] = SummarizerTool(twin_service)

    # Handle "Remote Supported" tools
    if mode == "remote" and tool_server_url:
        for name in REMOTE_SUPPORTED_TOOLS:
            tools[name] = RemoteToolProxy(name, tool_server_url)
    else:
        # Instantiate local versions of supported tools
        tools["ssh"] = SSH_Tool()
        tools["desktop_control"] = DesktopControlTool()
        tools["code_runner"] = CodeRunnerTool()
        tools["web_browser"] = WebBrowserTool()
        tools["ansible"] = Ansible_Tool()
        tools["power"] = Power_Tool()
        tools["term_everything"] = TermEverythingTool(app_image_path="/opt/mcp/termeverything.AppImage")

        # RAG Tool has specific local dependencies (memory)
        # Allow configurability for base_dir, but default to secure app dir
        rag_base_dir = config.get("rag_base_dir", "/opt/pipecatapp")
        rag_allowed_root = config.get("rag_allowed_root", rag_base_dir)
        tools["rag"] = RAG_Tool(
            pmm_memory=twin_service.long_term_memory if twin_service else None,
            base_dir=rag_base_dir,
            allowed_root=rag_allowed_root
        )

        tools["ha"] = HA_Tool(
            ha_url=config.get("ha_url"),
            ha_token=config.get("ha_token")
        )
        tools["git"] = Git_Tool(root_dir="/opt/pipecatapp")
        tools["orchestrator"] = OrchestratorTool()

    # Filter out None values
    return {k: v for k, v in tools.items() if v is not None}
