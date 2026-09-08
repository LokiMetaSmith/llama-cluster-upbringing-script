import asyncio
import base64
import json
import logging
import os
import time
from collections import defaultdict

import httpx
from opentelemetry import trace
from pipecat.frames.frames import TextFrame, TranscriptionFrame
from pipecat.processors.frame_processor import FrameProcessor

from pipecatapp.agent_factory import create_tools
from pipecatapp.net_utils import get_safe_url_and_headers, resolve_and_validate_url
from pipecatapp.pmm_memory import PMMMemory
from pipecatapp.pmm_memory_client import PMMMemoryClient
from pipecatapp.quality_control import CodeQualityAnalyzer
from pipecatapp.workflow.runner import ActiveWorkflows, WorkflowRunner

# Setup generic tracer for the application module
tracer = trace.get_tracer(__name__)

# -----------------------
# Session Locks
# -----------------------
session_locks = defaultdict(asyncio.Lock)


class TwinService(FrameProcessor):
    """Core conversational agent orchestrator.

    This class is the "brain" of the agent. It receives user input,
    initializes the workflow engine, and sends the final response.
    The core logic is now managed by the declarative workflow system.
    """
    def __init__(self, llm, vision_detector, runner, app_config: dict, approval_queue=None, llm_base_url=None, tts_service=None):
        """Initializes the TwinService.

        Args:
            llm: The primary LLM service client.
            vision_detector: An instance of YOLOv8Detector for scene analysis.
            runner: The Pipecat PipelineRunner instance.
            app_config (dict): The application's configuration loaded from Consul.
            approval_queue: The queue for handling tool use approval requests.
            llm_base_url (str, optional): The base URL of the LLM service.
            tts_service (FrameProcessor, optional): The TTS service for generating audio responses.
        """
        super().__init__()
        self.router_llm = llm
        self.llm_base_url = llm_base_url
        self.vision_detector = vision_detector
        self.runner = runner
        self.app_config = app_config or {}
        self.approval_queue = approval_queue
        self.tts_service = tts_service
        self.short_term_memory = []

        # Optimization: Pre-load external experts config to avoid json.loads in process_frame loop
        external_experts_config_str = os.getenv("EXTERNAL_EXPERTS_CONFIG", "{}")
        try:
            self.external_experts_config = json.loads(external_experts_config_str)
        except json.JSONDecodeError:
            self.external_experts_config = {}
            logging.warning("Failed to parse EXTERNAL_EXPERTS_CONFIG JSON.")

        # Check for sharded memory routing proxy
        enable_sharded = os.getenv("ENABLE_SHARDED_MEMORY", "false").lower() in ("true", "yes", "1")
        if enable_sharded:
            logging.info("ENABLE_SHARDED_MEMORY is true. Initializing ShardedPMMMemoryRouter.")
            try:
                import yaml
                try:
                    import pipecatapp.web_server
                except ImportError:
                    from pipecatapp import web_server
                from pipecatapp.sharded_router import ShardedPMMMemoryRouter
                config_path = os.getenv("SHARDING_CONFIG_PATH", "sharding_config.yaml")
                if not os.path.exists(config_path):
                    # Write a default mock sharding config for standalone/graceful fallback
                    default_config = {
                        "sharding": {
                            "algorithm": "consistent_hash",
                            "replica_count": 128,
                            "coordinator_node": "node_0",
                            "nodes": {
                                "node_0": {
                                    "sqlite_path": os.path.expanduser("~/.config/pipecat/pypicat_memory.db"),
                                    "api_url": "http://localhost:8000"
                                }
                            }
                        }
                    }
                    logging.warning(f"Sharding config {config_path} not found. Creating a default single-node sharding config.")
                    with open(config_path, "w") as f:
                        yaml.dump(default_config, f)

                router = ShardedPMMMemoryRouter(config_path)
                pipecatapp.web_server.app.state.memory_router = router
                self.long_term_memory = router
                logging.info(f"ShardedPMMMemoryRouter successfully initialized using {config_path}")
            except Exception as e:
                logging.error(f"Failed to initialize ShardedPMMMemoryRouter: {e}. Falling back to standard memory.")
                enable_sharded = False

        if not enable_sharded:
            # Use Remote Memory if available (via Consul discovery or env var), otherwise fallback to local
            memory_service_url = os.getenv("MEMORY_SERVICE_URL")
            if memory_service_url:
                 logging.info(f"Using Remote Memory Service at {memory_service_url}")
                 self.long_term_memory = PMMMemoryClient(base_url=memory_service_url)
            else:
                 logging.info("Using Local PMMMemory (SQLite)")
                 self.long_term_memory = PMMMemory(db_path="~/.config/pipecat/pypicat_memory.db")

        self.quality_analyzer = CodeQualityAnalyzer()

        # This will hold metadata from incoming requests (e.g., from the gateway)
        self.current_request_meta = None

        # Optimization: Reusable HTTP client for gateway responses
        self.http_client = httpx.AsyncClient(timeout=30.0)

        self.debug_mode = self.app_config.get("debug_mode", False)
        self.approval_mode = self.app_config.get("approval_mode", False)
        # Import dynamically if necessary to prevent circular dependencies
        from pipecatapp.net_utils import format_url
        self.consul_http_addr = format_url("http", self.app_config.get('consul_host', os.getenv('CLUSTER_IP', '127.0.0.1')), self.app_config.get('consul_port', 8500))

        # Initialize tools via factory
        self.tools = create_tools(self.app_config, twin_service=self, runner=self.runner, agent_name="main_app")
        # Add vision detector explicitly as it is a special case (frame processor)
        self.tools["vision"] = self.vision_detector

    def compact_session(self):
        """Compacts the short-term memory if it exceeds a certain token threshold."""
        # Estimate token count (roughly 4 chars per token)
        token_estimate = sum(len(str(m)) for m in self.short_term_memory) // 4

        # Arbitrary threshold for context length. Let's use 4000 tokens.
        if token_estimate < 4000:
            return

        logging.info("Compacting short-term memory...")
        split = len(self.short_term_memory) // 2
        old, recent = self.short_term_memory[:split], self.short_term_memory[split:]

        # Ensure summarizer tool is available before trying to use it
        summarizer = self.tools.get("summarizer")

        if summarizer and hasattr(summarizer, "get_summary"):
            # The summarizer extracts the top 3 most relevant turns. For a general
            # compaction, we just summarize everything we want to compact.
            # But the existing get_summary tool is an extractive summarizer focused on a query.
            # If we don't have a specific query, we can use a general string, or just keep recent
            summary_query = "important facts, decisions, and tasks"
            summary_text = summarizer.get_summary(summary_query, conversation_history=old)

            # get_summary might return a string starting with "Here are the most relevant points..."
            self.short_term_memory = [f"[Previous conversation summary]\n{summary_text}"] + recent
        else:
            # Fallback if no summarizer available: just truncate to keep recent half
            logging.info("No summarizer tool available; truncating short-term memory.")
            self.short_term_memory = ["[Older conversation history truncated]"] + recent

    def audit_log_tool_call(self, tool_name: str, args: dict, result: str, signature: str):
        """Appends a tamper-evident JSON log of the tool execution trace."""
        log_entry = {
            "timestamp": time.time(),
            "action": tool_name,
            "prompt": args,
            "response": result,
            "signature": signature
        }
        try:
            with open("audit.log", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logging.error(f"Failed to write to audit log: {e}")

    @tracer.start_as_current_span("TwinService.process_frame")
    async def process_frame(self, frame, direction):
        """Entry point for the agent's logic, triggered by a transcription frame.
        This now uses the new workflow engine.
        Args:
            frame: The incoming frame from the pipeline.
            direction: The direction of the frame in the pipeline.
        """
        span = trace.get_current_span()
        if not isinstance(frame, TranscriptionFrame):
            await self.push_frame(frame, direction)
            return

        span.set_attribute("agent.input_text", frame.text)

        # Compact memory before executing workflow
        self.compact_session()

        # Store meta for this request
        self.current_request_meta = frame.meta if hasattr(frame, 'meta') else None

        logging.info(f"Starting workflow for user query: {frame.text}")

        active_workflows = ActiveWorkflows()
        request_id = self.current_request_meta.get("request_id", str(time.time()))

        # Detect the requested workflow
        workflow_file = "workflows/default_agent_loop.yaml"
        if frame.text.strip().startswith("/deep"):
            logging.info("Deep Context / Slow Thinking mode activated.")
            workflow_file = "workflows/deep_context.yaml"
        elif frame.text.strip().startswith("/manager") or frame.text.strip().startswith("/openclaw"):
            logging.info("Project Manager / OpenClaw mode activated.")
            workflow_file = "workflows/manager.yaml"
        elif frame.text.strip().startswith("/sandbox"):
            logging.info("Sandbox Execution mode activated.")
            workflow_file = "workflows/sandbox.yaml"
        elif frame.text.strip().startswith(("/adversary", "/sim", "/redteam")):
            logging.info("Adversarial Simulation / Red Teaming mode activated.")
            workflow_file = "workflows/adversarial_simulation.yaml"

        session_id = self.current_request_meta.get("session_id", "default") if self.current_request_meta else "default"

        try:
            span.set_attribute("agent.workflow_file", workflow_file)
            span.set_attribute("agent.request_id", request_id)

            workflow_runner = WorkflowRunner(workflow_file, runner_id=request_id)
            active_workflows.add_runner(request_id, workflow_runner)

            global_inputs = {
                "user_text": frame.text,
                "tools_dict": self.tools,
                "tool_result": None, # Start with no tool result
                "consul_http_addr": self.consul_http_addr,
                "twin_service": self,
                "external_experts_config": self.external_experts_config
            }

            previous_tool_calls = []

            async with session_locks[session_id]:
                for step_idx in range(10): # Allow up to 10 steps in the thought process
                    with tracer.start_as_current_span(f"Workflow.Step_{step_idx}") as step_span:
                        workflow_result = await workflow_runner.run(global_inputs)

                        final_response = workflow_result.get("final_response")
                        if final_response:
                            step_span.set_attribute("workflow.final_response", final_response)

                        tool_call = workflow_result.get("tool_call")
                        if tool_call:
                            step_span.set_attribute("workflow.tool_call", str(tool_call.get("name")))

                    final_response = workflow_result.get("final_response")
                    tool_call = workflow_result.get("tool_call")

                    if final_response:
                        logging.info(f"Workflow produced final response: {final_response}")
                        await self._send_response(final_response)
                        await self.long_term_memory.add_event(kind="assistant_message", content=final_response)
                        self.short_term_memory.append(f"Assistant: {final_response}")
                        return # End the loop

                    if tool_call:
                        logging.info(f"Workflow produced tool call: {tool_call}")

                        # Detect Loops
                        tool_name = tool_call.get("name")
                        tool_args = tool_call.get("arguments", {})
                        # Normalize args to ensure consistent string representation
                        try:
                            tool_args_str = json.dumps(tool_args, sort_keys=True)
                        except Exception:
                            tool_args_str = str(tool_args)

                        current_signature = (tool_name, tool_args_str)
                        previous_tool_calls.append(current_signature)

                        # Check if the last 3 calls are identical
                        if len(previous_tool_calls) >= 3 and all(c == current_signature for c in previous_tool_calls[-3:]):
                            logging.warning("Loop detected in tool calls. Injecting system alert.")
                            global_inputs["tool_result"] = "SYSTEM ALERT: You have called this tool with these exact arguments 3 times in a row. Please change your strategy or ask the user for help."
                        else:
                            # The tool is executed within the workflow, so we just need to
                            # grab the result and feed it back into the next iteration.
                            global_inputs["tool_result"] = workflow_result.get("tool_result")

                            # Extract tool_receipt to log audit trail
                            tool_receipt = None
                            for node_id, outputs in workflow_runner.context.node_outputs.items():
                                if "tool_receipt" in outputs:
                                    tool_receipt = outputs["tool_receipt"]
                                    break

                            # Always log the audit trail even if receipt is None to maintain a complete record
                            if global_inputs.get("tool_result") is not None:
                                self.audit_log_tool_call(tool_name, tool_args, str(global_inputs["tool_result"]), tool_receipt)

                        # Continue the loop
                    else:
                        # This case should not be reached if the workflow is designed correctly
                        logging.error("Workflow ended without a final response or a tool call.")
                        await self._send_response("I'm sorry, my thought process ended unexpectedly.")
                        return

                # If the loop completes without a final answer
                await self._send_response("I seem to be stuck in a thought loop. Could you please clarify your request?")

        except Exception as e:
            logging.error(f"An error occurred during workflow execution: {e}", exc_info=True)
            await self._send_response("I'm sorry, an internal error occurred while processing your request with the new workflow engine.")
        finally:
            active_workflows.remove_runner(request_id)

    @tracer.start_as_current_span("TwinService._send_response")
    async def _send_response(self, text: str):
        """Sends a response back to the appropriate channel (TTS or Gateway)."""
        span = trace.get_current_span()
        span.set_attribute("agent.output_text", text)

        import pipecatapp.web_server
        if self.current_request_meta and self.current_request_meta.get("is_sync"):
            request_id = self.current_request_meta.get("request_id")
            if request_id and request_id in pipecatapp.web_server.sync_response_store:
                response_data = {"response": text}

                # Generate TTS if available
                if self.tts_service:
                    try:
                         # Use run_in_executor to avoid blocking
                         loop = asyncio.get_running_loop()
                         audio_bytes = await loop.run_in_executor(None, self.tts_service._synthesize_sync, text)
                         audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
                         response_data["audio_base64"] = audio_b64
                    except Exception as e:
                         logging.error(f"TTS generation failed for sync response: {e}")

                pipecatapp.web_server.sync_response_store[request_id]["response"] = response_data
                pipecatapp.web_server.sync_response_store[request_id]["event"].set()
                logging.info(f"Set synchronous response for request {request_id}")
            else:
                logging.warning(f"Sync response request {request_id} not found in store.")
        elif self.current_request_meta and "response_url" in self.current_request_meta:
            response_url = self.current_request_meta["response_url"]
            request_id = self.current_request_meta["request_id"]

            try:
                # Security Fix: Sentinel - Validate URL and use resolved IP for HTTP to prevent DNS Rebinding
                original_url, safe_ip = await resolve_and_validate_url(response_url)
                safe_url, headers = get_safe_url_and_headers(original_url, safe_ip)
            except ValueError as e:
                logging.error(f"Blocked SSRF attempt in response_url: {e}")
                return

            response_payload = {"request_id": request_id, "content": text}

            # Generate TTS if available
            if self.tts_service:
                 try:
                     loop = asyncio.get_running_loop()
                     audio_bytes = await loop.run_in_executor(None, self.tts_service._synthesize_sync, text)
                     audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
                     response_payload["audio_base64"] = audio_b64
                 except Exception as e:
                     logging.error(f"TTS generation failed for callback response: {e}")

            try:
                # Bolt ⚡ Optimization: Use reused client instead of creating new one
                await self.http_client.post(safe_url, json=response_payload, headers=headers)
                logging.info(f"Sent response for request {request_id} to gateway.")
            except Exception as e:
                logging.error(f"Failed to send response to gateway: {e}")
        else:
            # Default to pushing to the audio pipeline
            await self.push_frame(TextFrame(text))

    async def _request_approval(self, tool_call_info: dict) -> bool:
        """Sends a tool call to the web UI for user approval.

        Args:
            tool_call_info (dict): A dictionary describing the tool call.

        Returns:
            True if the user approved the action, False otherwise.
        """
        import pipecatapp.web_server
        request_id = str(time.time())
        await pipecatapp.web_server.manager.broadcast(json.dumps({"type": "approval_request", "data": {"request_id": request_id, "tool_call": tool_call_info}}))
        while True:
            response = await self.approval_queue.get()
            if response.get("data", {}).get("request_id") == request_id:
                return response.get("data", {}).get("approved", False)
