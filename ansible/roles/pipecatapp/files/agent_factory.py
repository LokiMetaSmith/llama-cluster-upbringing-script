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

    tools = {
        "ssh": SSH_Tool(),
        # MCP Tool needs runner and twin_service
        "mcp": MCP_Tool(twin_service, runner) if twin_service and runner else None,
        # Vision is usually handled separately (YOLO), but we can add placeholders or simple tools
        # "vision": ... (In app.py it's the YOLO detector instance itself)
        "desktop_control": DesktopControlTool(),
        "code_runner": CodeRunnerTool(),
        "smol_agent_computer": SmolAgentTool(),
        "web_browser": WebBrowserTool(),
        "ansible": Ansible_Tool(),
        "power": Power_Tool(),
        "term_everything": TermEverythingTool(app_image_path="/opt/mcp/termeverything.AppImage"),
        "rag": RAG_Tool(pmm_memory=twin_service.long_term_memory if twin_service else None, base_dir="/"),
        "ha": HA_Tool(
            ha_url=config.get("ha_url"),
            ha_token=config.get("ha_token")
        ),
        "git": Git_Tool(),
        "orchestrator": OrchestratorTool(),
        "llxprt_code": LLxprt_Code_Tool(),
        "claude_clone": ClaudeCloneTool(),
        "final_answer": FinalAnswerTool(),
        "shell": ShellTool(),
        "prompt_improver": PromptImproverTool(twin_service) if twin_service else None,
        "council": CouncilTool(twin_service) if twin_service else None,
        "swarm": SwarmTool(),
        "project_mapper": ProjectMapperTool(),
        "planner": PlannerTool(twin_service) if twin_service else None,
        "file_editor": FileEditorTool(root_dir="/opt/pipecatapp"), # Allow editing within the app dir
    }

    if config.get("use_summarizer", False) and twin_service:
        tools["summarizer"] = SummarizerTool(twin_service)

    # Filter out None values
    return {k: v for k, v in tools.items() if v is not None}
