import os
import sys
import importlib
import logging

# Tools that are supported by the Tool Server and can be proxied
REMOTE_SUPPORTED_TOOLS = [
    "ssh", "desktop_control", "code_runner", "web_browser",
    "ansible", "power", "term_everything", "rag", "ha",
    "git", "orchestrator", "opencode_provider",
    "ocr", "wasm", "heretic"
]

# Heavy tools that should ideally be offloaded to the Tool Server for microservice de-monolithization
HEAVY_TOOLS = ["rag", "code_runner", "ansible", "ocr", "wasm", "heretic"]

TOOL_CLASS_MAP = {
    "SSH_Tool": ("pipecatapp.tools.ssh_tool", "SSH_Tool"),
    "MCP_Tool": ("pipecatapp.tools.mcp_tool", "MCP_Tool"),
    "DesktopControlTool": ("pipecatapp.tools.desktop_control_tool", "DesktopControlTool"),
    "CodeRunnerTool": ("pipecatapp.tools.code_runner_tool", "CodeRunnerTool"),
    "WebBrowserTool": ("pipecatapp.tools.web_browser_tool", "WebBrowserTool"),
    "Ansible_Tool": ("pipecatapp.tools.ansible_tool", "Ansible_Tool"),
    "AnsibleExceptionHandlerTool": ("pipecatapp.tools.ansible_exception_handler_tool", "AnsibleExceptionHandlerTool"),
    "Power_Tool": ("pipecatapp.tools.power_tool", "Power_Tool"),
    "SummarizerTool": ("pipecatapp.tools.summarizer_tool", "SummarizerTool"),
    "TermEverythingTool": ("pipecatapp.tools.term_everything_tool", "TermEverythingTool"),
    "RAG_Tool": ("pipecatapp.tools.rag_tool", "RAG_Tool"),
    "RAGPruner": ("pipecatapp.utils.rag_pruner", "RAGPruner"),
    "ExternalLLMClient": ("pipecatapp.llm_clients", "ExternalLLMClient"),
    "HA_Tool": ("pipecatapp.tools.ha_tool", "HA_Tool"),
    "Git_Tool": ("pipecatapp.tools.git_tool", "Git_Tool"),
    "OrchestratorTool": ("pipecatapp.tools.orchestrator_tool", "OrchestratorTool"),
    "LLxprt_Code_Tool": ("pipecatapp.tools.llxprt_code_tool", "LLxprt_Code_Tool"),
    "SmolAgentTool": ("pipecatapp.tools.smol_agent_tool", "SmolAgentTool"),
    "MiniSWEAgentTool": ("pipecatapp.tools.mini_swe_tool", "MiniSWEAgentTool"),
    "FinalAnswerTool": ("pipecatapp.tools.final_answer_tool", "FinalAnswerTool"),
    "MCPClientAdapter": ("pipecatapp.tools.mcp_client_adapter", "MCPClientAdapter"),
    "PromptImproverTool": ("pipecatapp.tools.prompt_improver_tool", "PromptImproverTool"),
    "CouncilTool": ("pipecatapp.tools.council_tool", "CouncilTool"),
    "SwarmTool": ("pipecatapp.tools.swarm_tool", "SwarmTool"),
    "HolographicMemoryTool": ("pipecatapp.tools.holographic_memory_tool", "HolographicMemoryTool"),
    "SubstrateVisualizerTool": ("pipecatapp.tools.substrate_visualizer_tool", "SubstrateVisualizerTool"),
    "ProjectMapperTool": ("pipecatapp.tools.project_mapper_tool", "ProjectMapperTool"),
    "PlannerTool": ("pipecatapp.tools.planner_tool", "PlannerTool"),
    "FileEditorTool": ("pipecatapp.tools.file_editor_tool", "FileEditorTool"),
    "SecurityRemediationTool": ("pipecatapp.tools.security_remediation_tool", "SecurityRemediationTool"),
    "NetworkInvestigatorTool": ("pipecatapp.tools.network_investigator_tool", "NetworkInvestigatorTool"),
    "ProcessInvestigatorTool": ("pipecatapp.tools.process_investigator_tool", "ProcessInvestigatorTool"),
    "ArchivistTool": ("pipecatapp.tools.archivist_tool", "ArchivistTool"),
    "OpencodeTool": ("pipecatapp.tools.opencode_tool", "OpencodeTool"),
    "OpenCodeProviderTool": ("pipecatapp.tools.opencode_provider_tool", "OpenCodeProviderTool"),
    "DependencyScannerTool": ("pipecatapp.tools.dependency_scanner_tool", "DependencyScannerTool"),
    "RemoteToolProxy": ("pipecatapp.tools.remote_tool_proxy", "RemoteToolProxy"),
    "VRTool": ("pipecatapp.tools.vr_tool", "VRTool"),
    "ExperimentTool": ("pipecatapp.tools.experiment_tool", "ExperimentTool"),
    "AutoresearchTool": ("pipecatapp.tools.autoresearch_tool", "AutoresearchTool"),
    "SubmitSolutionTool": ("pipecatapp.tools.submit_solution_tool", "SubmitSolutionTool"),
    "ContainerRegistryTool": ("pipecatapp.tools.container_registry_tool", "ContainerRegistryTool"),
    "SearchTool": ("pipecatapp.tools.search_tool", "SearchTool"),
    "MTACTool": ("pipecatapp.tools.mtac_tool", "MTACTool"),
    "OpenClawTool": ("pipecatapp.tools.openclaw_tool", "OpenClawTool"),
    "ATProtoTool": ("pipecatapp.tools.atproto_tool", "ATProtoTool"),
    "SchedulerTool": ("pipecatapp.tools.scheduler_tool", "SchedulerTool"),
    "ContextUploadTool": ("pipecatapp.tools.context_upload_tool", "ContextUploadTool"),
    "PersonalityTool": ("pipecatapp.tools.personality_tool", "PersonalityTool"),
    "SaveSkillTool": ("pipecatapp.tools.save_skill_tool", "SaveSkillTool"),
    "SearchSkillsTool": ("pipecatapp.tools.search_skills_tool", "SearchSkillsTool"),
    "Last30DaysTool": ("pipecatapp.tools.last30days_tool", "Last30DaysTool"),
    "WOLTool": ("pipecatapp.tools.wol_tool", "WOLTool"),
    "ScaleComputeTool": ("pipecatapp.tools.scale_compute_tool", "ScaleComputeTool"),
    "ClusterStatusTool": ("pipecatapp.tools.cluster_status_tool", "ClusterStatusTool"),
    "PolyphonyTool": ("pipecatapp.tools.polyphony_tool", "PolyphonyTool"),
    "SkillBuilderTool": ("pipecatapp.tools.skill_builder_tool", "SkillBuilderTool"),
    "DynamicSkillTool": ("pipecatapp.tools.dynamic_skill_tool", "DynamicSkillTool"),
    "ASTEditorTool": ("pipecatapp.tools.ast_editor_tool", "ASTEditorTool"),
    "ShuntTool": ("pipecatapp.tools.shunt_tool", "ShuntTool"),
    "LightweightProjectMapperTool": ("pipecatapp.tools.lightweight_project_mapper_tool", "LightweightProjectMapperTool"),
    "SchemaHarnessTool": ("pipecatapp.tools.schema_harness_tool", "SchemaHarnessTool"),
    "SchemaMapperTool": ("pipecatapp.tools.schema_mapper_tool", "SchemaMapperTool"),
    "SetOperationalModeTool": ("pipecatapp.tools.set_operational_mode_tool", "SetOperationalModeTool"),
    "OuroborosTool": ("pipecatapp.tools.ouroboros_tool", "OuroborosTool"),
    "TernlightTool": ("pipecatapp.tools.ternlight_tool", "TernlightTool"),
    "ExternalAppManagerTool": ("pipecatapp.tools.external_app_manager_tool", "ExternalAppManagerTool"),
    "JacobianLensTool": ("pipecatapp.tools.jacobian_lens_tool", "JacobianLensTool"),
    "WasmTool": ("pipecatapp.tools.wasm_tool", "WasmTool"),
    "AutoloopTool": ("pipecatapp.tools.autoloop_tool", "AutoloopTool"),
    "CQ_Tool": ("pipecatapp.tools.cq_tool", "CQ_Tool"),
    "DocumentTool": ("pipecatapp.tools.document_tool", "DocumentTool"),
    "HereticTool": ("pipecatapp.tools.heretic_tool", "HereticTool"),
    "JulesTool": ("pipecatapp.tools.jules_tool", "JulesTool"),
    "OCRTool": ("pipecatapp.tools.ocr_tool", "OCRTool"),
    "OpenWorkersTool": ("pipecatapp.tools.open_workers_tool", "OpenWorkersTool"),
    "P2PSyncTool": ("pipecatapp.tools.p2p_sync_tool", "P2PSyncTool"),
    "ProjectOverviewTool": ("pipecatapp.tools.project_overview_tool", "ProjectOverviewTool"),
    "SpecLoaderTool": ("pipecatapp.tools.spec_loader_tool", "SpecLoaderTool"),
    "UpdateLitellmTool": ("pipecatapp.tools.update_litellm_tool", "UpdateLitellmTool"),
    "GetNomadJobTool": ("pipecatapp.tools.get_nomad_job", "GetNomadJobTool"),
    "FrugalSandboxTool": ("pipecatapp.tools.frugal_sandbox_tool", "FrugalSandboxTool"),
    "GoalTool": ("pipecatapp.tools.goal_tool", "GoalTool"),
    "FieldGuideTool": ("pipecatapp.tools.field_guide_tool", "FieldGuideTool"),
    "DesignDocsTool": ("pipecatapp.tools.design_docs_tool", "DesignDocsTool"),
    "GitCoordinationTool": ("pipecatapp.tools.git_coordination_tool", "GitCoordinationTool"),
    "UnitReasoningTool": ("pipecatapp.tools.unit_reasoning_tool", "UnitReasoningTool"),
    "SSDStreamingTool": ("pipecatapp.tools.ssd_streaming_tool", "SSDStreamingTool"),
}

_loaded_classes = {}

def __getattr__(name: str):
    if name in _loaded_classes:
        return _loaded_classes[name]
    if name in TOOL_CLASS_MAP:
        mod_name, cls_name = TOOL_CLASS_MAP[name]
        try:
            mod = importlib.import_module(mod_name)
            cls = getattr(mod, cls_name)
            _loaded_classes[name] = cls
            return cls
        except Exception as e:
            logging.warning(f"Could not load tool class {name} from {mod_name}: {e}")
            class _UnavailableTool:
                def __init__(self, *args, **kwargs):
                    self.name = name.lower()
                    self.available = False
                    self.load_error = str(e)
                def __call__(self, *args, **kwargs):
                    return self
            _UnavailableTool.__name__ = cls_name
            _loaded_classes[name] = _UnavailableTool
            return _UnavailableTool
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def _get_cls(name: str):
    """Retrieve class from module dict (respecting patches) or lazy loader."""
    this_mod = sys.modules[__name__]
    return getattr(this_mod, name)


def _safe_create(tool_name: str, factory_fn):
    """Safely instantiate a tool, catching errors so app boot doesn't crash."""
    try:
        instance = factory_fn()
        return instance
    except Exception as e:
        logging.warning(f"Optional tool '{tool_name}' could not be initialized: {e}")
        return None


def create_tools(config: dict | None = None, twin_service=None, runner=None, agent_name: str | None = None) -> dict:
    """
    Initializes and returns the dictionary of tools.

    Args:
        config (dict): Configuration dictionary (e.g. from Consul).
        twin_service: Reference to the agent/service using the tools (optional).
        runner: Reference to the pipeline runner (optional).
        agent_name (str): The name of the agent calling this, for identity mapping (optional).

    Returns:
        dict: A dictionary of tool instances.
    """
    if config is None:
        config = {}

    mode = config.get("tool_execution_mode", "local")
    tool_server_url = config.get("tool_server_url")

    tools = {}

    # Local base tools
    tools["frugal_sandbox"] = _safe_create("frugal_sandbox", lambda: _get_cls("FrugalSandboxTool")())
    tools["goal"] = _safe_create("goal", lambda: _get_cls("GoalTool")())
    if twin_service and runner:
        tools["mcp"] = _safe_create("mcp", lambda: _get_cls("MCP_Tool")(twin_service, runner))
    tools["smol_agent_computer"] = _safe_create("smol_agent_computer", lambda: _get_cls("SmolAgentTool")())
    tools["mini_swe_agent"] = _safe_create("mini_swe_agent", lambda: _get_cls("MiniSWEAgentTool")())
    tools["llxprt_code"] = _safe_create("llxprt_code", lambda: _get_cls("LLxprt_Code_Tool")())
    tools["final_answer"] = _safe_create("final_answer", lambda: _get_cls("FinalAnswerTool")())
    tools["holographic_memory"] = _safe_create("holographic_memory", lambda: _get_cls("HolographicMemoryTool")())
    tools["substrate_visualizer"] = _safe_create("substrate_visualizer", lambda: _get_cls("SubstrateVisualizerTool")())
    tools["shell"] = _safe_create("shell", lambda: _get_cls("MCPClientAdapter")(
        name="shell",
        server_command="python3",
        server_args=["-m", "servers.shell_server"],
        description=(
            "A tool for running shell commands in a persistent tmux session. "
            "IMPORTANT: If running a long-running process (like a server), you MUST run it in the background "
            "by appending `&` to the command and redirecting output to a file (e.g., `npm start > app.log 2>&1 &`). "
            "Do not wait synchronously for long-running processes or the tool will timeout."
        ),
        twin_service=twin_service
    ))
    if twin_service:
        tools["prompt_improver"] = _safe_create("prompt_improver", lambda: _get_cls("PromptImproverTool")(twin_service))
        tools["council"] = _safe_create("council", lambda: _get_cls("CouncilTool")(twin_service))
        tools["planner"] = _safe_create("planner", lambda: _get_cls("PlannerTool")(twin_service))
    tools["swarm"] = _safe_create("swarm", lambda: _get_cls("SwarmTool")())
    tools["project_mapper"] = _safe_create("project_mapper", lambda: _get_cls("ProjectMapperTool")())
    tools["lightweight_project_mapper"] = _safe_create("lightweight_project_mapper", lambda: _get_cls("LightweightProjectMapperTool")())
    tools["schema_harness"] = _safe_create("schema_harness", lambda: _get_cls("SchemaHarnessTool")())
    tools["field_guide"] = _safe_create("field_guide", lambda: _get_cls("FieldGuideTool")())
    tools["design_docs"] = _safe_create("design_docs", lambda: _get_cls("DesignDocsTool")())
    tools["git_coordination"] = _safe_create("git_coordination", lambda: _get_cls("GitCoordinationTool")())
    tools["unit_reasoning"] = _safe_create("unit_reasoning", lambda: _get_cls("UnitReasoningTool")())
    tools["ssd_streaming"] = _safe_create("ssd_streaming", lambda: _get_cls("SSDStreamingTool")())
    tools["schema_mapper"] = _safe_create("schema_mapper", lambda: _get_cls("SchemaMapperTool")())
    tools["file_editor"] = _safe_create("file_editor", lambda: _get_cls("FileEditorTool")(root_dir="/opt/pipecatapp"))
    tools["shunt"] = _safe_create("shunt", lambda: _get_cls("ShuntTool")())
    tools["file_editor_mcp"] = _safe_create("file_editor_mcp", lambda: _get_cls("MCPClientAdapter")(
        name="file_editor_mcp",
        server_command="python3",
        server_args=["-m", "pipecatapp.servers.file_editor_server"],
        description="Reads, writes, and patches files in the codebase using MCP.",
        twin_service=twin_service
    ))
    tools["security_remediation"] = _safe_create("security_remediation", lambda: _get_cls("SecurityRemediationTool")())
    tools["network_investigator"] = _safe_create("network_investigator", lambda: _get_cls("NetworkInvestigatorTool")())
    tools["process_investigator"] = _safe_create("process_investigator", lambda: _get_cls("ProcessInvestigatorTool")())
    tools["archivist"] = _safe_create("archivist", lambda: _get_cls("ArchivistTool")())
    tools["opencode"] = _safe_create("opencode", lambda: _get_cls("OpencodeTool")(
        base_url=config.get("opencode_api_url"),
        provider_id=config.get("opencode_provider", "openai"),
        model_id=config.get("opencode_model", "gpt-4o")
    ))
    tools["opencode_provider"] = _safe_create("opencode_provider", lambda: _get_cls("OpenCodeProviderTool")())
    tools["dependency_scanner"] = _safe_create("dependency_scanner", lambda: _get_cls("DependencyScannerTool")())
    tools["vr"] = _safe_create("vr", lambda: _get_cls("VRTool")())
    tools["autoresearch"] = _safe_create("autoresearch", lambda: _get_cls("AutoresearchTool")(
        llm_client=getattr(twin_service, 'moe_llm', None) if twin_service else None
    ))
    tools["experiment"] = _safe_create("experiment", lambda: _get_cls("ExperimentTool")())
    tools["submit_solution"] = _safe_create("submit_solution", lambda: _get_cls("SubmitSolutionTool")())
    tools["container_registry"] = _safe_create("container_registry", lambda: _get_cls("ContainerRegistryTool")())
    tools["search"] = _safe_create("search", lambda: _get_cls("SearchTool")(root_dir="/opt/pipecatapp"))
    tools["mtac"] = _safe_create("mtac", lambda: _get_cls("MTACTool")())
    tools["openclaw"] = _safe_create("openclaw", lambda: _get_cls("OpenClawTool")(
        gateway_url=config.get("openclaw_gateway_url", "ws://openclaw.service.consul:18789")
    ))
    tools["atproto"] = _safe_create("atproto", lambda: _get_cls("ATProtoTool")(
        username=config.get("pds_identities", {}).get(agent_name, config.get("pds_username", "")) if agent_name else config.get("pds_username", ""),
        password=config.get("pds_passwords", {}).get(agent_name, config.get("pds_password", "")) if agent_name else config.get("pds_password", ""),
        pds_url=config.get("pds_url", "https://pds.local")
    ))
    tools["scheduler"] = _safe_create("scheduler", lambda: _get_cls("SchedulerTool")())
    tools["context_upload"] = _safe_create("context_upload", lambda: _get_cls("ContextUploadTool")())
    tools["personality"] = _safe_create("personality", lambda: _get_cls("PersonalityTool")(api_url=config.get("llama_api_url")))
    tools["save_skill"] = _safe_create("save_skill", lambda: _get_cls("SaveSkillTool")())
    tools["search_skills"] = _safe_create("search_skills", lambda: _get_cls("SearchSkillsTool")())
    tools["last30days"] = _safe_create("last30days", lambda: _get_cls("Last30DaysTool")(
        service_url=config.get("last30days_service_url", "http://last30days-service.service.consul:8008"),
        api_key=config.get("tool_server_api_key") or os.getenv("TOOL_SERVER_API_KEY")
    ))
    tools["wol"] = _safe_create("wol", lambda: _get_cls("WOLTool")())
    tools["scale_compute"] = _safe_create("scale_compute", lambda: _get_cls("ScaleComputeTool")())
    tools["cluster_status"] = _safe_create("cluster_status", lambda: _get_cls("ClusterStatusTool")())
    tools["polyphony"] = _safe_create("polyphony", lambda: _get_cls("PolyphonyTool")())
    tools["skill_builder"] = _safe_create("skill_builder", lambda: _get_cls("SkillBuilderTool")())
    tools["ast_editor"] = _safe_create("ast_editor", lambda: _get_cls("ASTEditorTool")(root_dir="/opt/pipecatapp"))
    tools["set_operational_mode"] = _safe_create("set_operational_mode", lambda: _get_cls("SetOperationalModeTool")())
    tools["ouroboros"] = _safe_create("ouroboros", lambda: _get_cls("OuroborosTool")(
        consul_host=config.get('consul_host'),
        consul_port=config.get('consul_port', 8500)
    ))
    tools["ternlight"] = _safe_create("ternlight", lambda: _get_cls("TernlightTool")(
        base_url=config.get("ternlight_service_url")
    ))
    tools["external_app_manager"] = _safe_create("external_app_manager", lambda: _get_cls("ExternalAppManagerTool")(
        consul_url=config.get('consul_url'),
        nomad_url=config.get('nomad_url')
    ))
    tools["jacobian_lens"] = _safe_create("jacobian_lens", lambda: _get_cls("JacobianLensTool")())
    tools["wasm"] = _safe_create("wasm", lambda: _get_cls("WasmTool")(wasm_path=config.get("wasm_path")))
    tools["autoloop"] = _safe_create("autoloop", lambda: _get_cls("AutoloopTool")())
    tools["cq"] = _safe_create("cq", lambda: _get_cls("CQ_Tool")())
    tools["document"] = _safe_create("document", lambda: _get_cls("DocumentTool")(
        backend_config=config.get("document_backend", {"type": "local", "directory": "/opt/pipecatapp" if os.path.exists("/opt/pipecatapp") else os.getcwd()})
    ))
    tools["document_mcp"] = _safe_create("document_mcp", lambda: _get_cls("MCPClientAdapter")(
        name="document_mcp",
        server_command="python3",
        server_args=["-m", "pipecatapp.servers.document_server"],
        description="Searches and reads internal documents or code files using MCP.",
        twin_service=twin_service
    ))
    tools["heretic"] = _safe_create("heretic", lambda: _get_cls("HereticTool")(root_dir=config.get("heretic_root_dir")))
    tools["jules"] = _safe_create("jules", lambda: _get_cls("JulesTool")(api_key=config.get("jules_api_key")))
    tools["ansible_exception_handler"] = _safe_create("ansible_exception_handler", lambda: _get_cls("AnsibleExceptionHandlerTool")())
    tools["ocr"] = _safe_create("ocr", lambda: _get_cls("OCRTool")())
    tools["openworkers"] = _safe_create("openworkers", lambda: _get_cls("OpenWorkersTool")(
        api_url=config.get("openworkers_api_url"),
        token=config.get("openworkers_token")
    ))
    tools["p2p_sync"] = _safe_create("p2p_sync", lambda: _get_cls("P2PSyncTool")(
        base_dir=config.get("p2p_sync_base_dir"),
        gui_port=config.get("p2p_sync_gui_port", 8384),
        listen_port=config.get("p2p_sync_listen_port", 22000)
    ))
    tools["project_overview"] = _safe_create("project_overview", lambda: _get_cls("ProjectOverviewTool")())
    tools["spec_loader"] = _safe_create("spec_loader", lambda: _get_cls("SpecLoaderTool")(
        work_dir=config.get("spec_loader_work_dir", "/opt/pipecatapp/specs")
    ))
    tools["update_litellm"] = _safe_create("update_litellm", lambda: _get_cls("UpdateLitellmTool")())
    tools["get_nomad_job"] = _safe_create("get_nomad_job", lambda: _get_cls("GetNomadJobTool")())

    # Inject memory client into SwarmTool if available (for Map-Reduce)
    if tools.get("swarm") and twin_service and hasattr(twin_service, "long_term_memory"):
        tools["swarm"].memory_client = twin_service.long_term_memory

    if config.get("use_summarizer", False) and twin_service:
        tools["summarizer"] = _safe_create("summarizer", lambda: _get_cls("SummarizerTool")(twin_service))

    # Handle "Remote Supported" tools
    if mode == "remote" and tool_server_url:
        for name in REMOTE_SUPPORTED_TOOLS:
            remote_proxy_cls = _get_cls("RemoteToolProxy")
            tools[name] = remote_proxy_cls(name, tool_server_url)
    else:
        # We are in local or mixed mode. Offload HEAVY_TOOLS if a tool_server_url is available.
        for name in REMOTE_SUPPORTED_TOOLS:
            if name in HEAVY_TOOLS and tool_server_url:
                remote_proxy_cls = _get_cls("RemoteToolProxy")
                tools[name] = remote_proxy_cls(name, tool_server_url)
            else:
                # Instantiate local versions of supported tools
                if name == "ssh":
                    tools["ssh"] = _safe_create("ssh", lambda: _get_cls("SSH_Tool")())
                elif name == "desktop_control":
                    tools["desktop_control"] = _safe_create("desktop_control", lambda: _get_cls("DesktopControlTool")())
                elif name == "code_runner":
                    tools["code_runner"] = _safe_create("code_runner", lambda: _get_cls("CodeRunnerTool")())
                    tools["code_runner_mcp"] = _safe_create("code_runner_mcp", lambda: _get_cls("MCPClientAdapter")(
                        name="code_runner_mcp",
                        server_command="python3",
                        server_args=["-m", "pipecatapp.servers.code_runner_server"],
                        description="Execute Python code in a sandboxed Docker/Nomad container using MCP.",
                        twin_service=twin_service
                    ))
                elif name == "web_browser":
                    tools["web_browser"] = _safe_create("web_browser", lambda: _get_cls("WebBrowserTool")())
                elif name == "ansible":
                    tools["ansible"] = _safe_create("ansible", lambda: _get_cls("Ansible_Tool")())
                elif name == "power":
                    tools["power"] = _safe_create("power", lambda: _get_cls("Power_Tool")())
                elif name == "term_everything":
                    tools["term_everything"] = _safe_create("term_everything", lambda: _get_cls("TermEverythingTool")(app_image_path="/opt/mcp/termeverything.AppImage"))
                elif name == "rag":
                    def _init_rag():
                        rag_base_dir = config.get("rag_base_dir", "/opt/pipecatapp")
                        rag_allowed_root = config.get("rag_allowed_root", rag_base_dir)
                        pruner = None
                        pruner_model = config.get("rag_pruner_model")
                        if pruner_model:
                            pruner_base_url = config.get("rag_pruner_base_url")
                            if not pruner_base_url:
                                pruner_base_url = os.getenv("LLAMA_API_BASE_URL") or config.get("llama_api_url")
                            pruner_api_key = config.get("rag_pruner_api_key") or os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY") or "dummy"
                            if pruner_base_url and pruner_model:
                                llm_client = _get_cls("ExternalLLMClient")(
                                    base_url=pruner_base_url,
                                    api_key=pruner_api_key,
                                    model=pruner_model
                                )
                                pruner = _get_cls("RAGPruner")(llm_client=llm_client)

                        rag_tool = _get_cls("RAG_Tool")(
                            pmm_memory=twin_service.long_term_memory if twin_service else None,
                            base_dir=rag_base_dir,
                            allowed_root=rag_allowed_root,
                            pruner=pruner,
                            pruning_threshold=config.get("rag_pruning_threshold", 4),
                            keep_top_k=config.get("rag_keep_top_k", 3)
                        )
                        return rag_tool
                    tools["rag"] = _safe_create("rag", _init_rag)
                    tools["rag_mcp"] = _safe_create("rag_mcp", lambda: _get_cls("MCPClientAdapter")(
                        name="rag_mcp",
                        server_command="python3",
                        server_args=["-m", "pipecatapp.servers.rag_server"],
                        description="Retrieves information from a project-specific knowledge base using MCP.",
                        twin_service=twin_service
                    ))
                elif name == "ha":
                    tools["ha"] = _safe_create("ha", lambda: _get_cls("HA_Tool")(
                        ha_url=config.get("ha_url"),
                        ha_token=config.get("ha_token")
                    ))
                elif name == "git":
                    tools["git"] = _safe_create("git", lambda: _get_cls("Git_Tool")(root_dir="/opt/pipecatapp"))
                elif name == "orchestrator":
                    def _init_orchestrator():
                        world_model = None
                        try:
                            from pipecatapp.app import app as main_app
                            world_model = getattr(main_app.state, 'world_model', None)
                        except ImportError:
                            pass
                        return _get_cls("OrchestratorTool")(world_model=world_model)
                    tools["orchestrator"] = _safe_create("orchestrator", _init_orchestrator)
                elif name == "opencode_provider":
                    tools["opencode_provider"] = _safe_create("opencode_provider", lambda: _get_cls("OpenCodeProviderTool")())

    # Load dynamic skills from memory store
    if twin_service and hasattr(twin_service, "long_term_memory"):
        try:
            dynamic_skills = twin_service.long_term_memory.list_skills()
            dyn_tool_cls = _get_cls("DynamicSkillTool")
            for skill in dynamic_skills:
                if skill["name"] not in tools:
                    tools[skill["name"]] = dyn_tool_cls(
                        name=skill["name"],
                        description=skill["description"],
                        content=twin_service.long_term_memory.get_skill(skill["name"])["content"],
                        code_runner=tools.get("code_runner")
                    )
        except Exception as e:
            logging.warning(f"Failed to load dynamic skills: {e}")

    # Filter out None values
    return {k: v for k, v in tools.items() if v is not None}
