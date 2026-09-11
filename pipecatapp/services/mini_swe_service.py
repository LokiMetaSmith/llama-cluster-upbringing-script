"""
Mini-SWE-Agent Service Integration Module for PipecatApp.

Provides an interface for executing code repair and bash-based agent tasks using mini-swe-agent,
configured to talk to the local MoE Gateway or external LLMs, with Docker sandboxing by default.
"""

import os
import logging
from typing import Dict, Any, Optional

from minisweagent.agents.default import DefaultAgent
from minisweagent.environments.local import LocalEnvironment
from minisweagent.environments.docker import DockerEnvironment
from minisweagent.models.litellm_model import LitellmModel

logger = logging.getLogger(__name__)

DEFAULT_MOE_GATEWAY_URL = os.getenv("MOE_GATEWAY_URL") or os.getenv("LLM_BASE_URL") or f"http://{os.getenv('CLUSTER_IP', '127.0.0.1')}:8081/v1"
DEFAULT_MODEL_NAME = os.getenv("MINI_SWE_MODEL", "openai/gpt-4o-mini")

class MiniSWEService:
    """
    Wrapper service around mini-swe-agent providing unified task execution,
    MoE Gateway model configuration, and isolated sandbox support.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        api_base: Optional[str] = None,
        environment_type: str = "docker",
        container_image: str = "python:3.12-slim",
        cwd: Optional[str] = None,
    ):
        self.model_name = model_name or DEFAULT_MODEL_NAME
        self.api_base = api_base or DEFAULT_MOE_GATEWAY_URL
        self.environment_type = environment_type.lower()
        self.container_image = container_image
        self.cwd = cwd or os.getcwd()

    def _get_model(self) -> LitellmModel:
        """Initialize LiteLLM model pointing to MoE Gateway or configured endpoint."""
        model_kwargs = {
            "model_name": self.model_name,
        }
        if self.api_base:
            model_kwargs["api_base"] = self.api_base
        return LitellmModel(**model_kwargs)

    def _get_environment(self, cwd: Optional[str] = None):
        """
        Instantiate execution environment based on configured environment type.
        Defaults to DockerEnvironment for sandboxing; falls back to LocalEnvironment
        for trusted execution.
        """
        work_dir = cwd or self.cwd
        if self.environment_type == "local":
            logger.info("Using LocalEnvironment for mini-swe-agent (trusted execution)")
            return LocalEnvironment(cwd=work_dir)
        else:
            logger.info("Using DockerEnvironment for mini-swe-agent (sandboxed execution)")
            return DockerEnvironment(image=self.container_image, cwd=work_dir)

    def run_task(
        self,
        task: str,
        cwd: Optional[str] = None,
        environment_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute a coding/repair task using mini-swe-agent.
        Returns execution result summary.
        """
        env_type = environment_type or self.environment_type
        saved_env_type = self.environment_type
        self.environment_type = env_type.lower()

        try:
            model = self._get_model()
            environment = self._get_environment(cwd=cwd)
            agent = DefaultAgent(model=model, env=environment)

            logger.info(f"Running mini-swe-agent task: {task[:80]}...")
            trajectory = agent.run(task)
            return {
                "status": "success",
                "task": task,
                "environment_type": self.environment_type,
                "trajectory": trajectory,
            }
        except Exception as e:
            logger.error(f"Error running mini-swe-agent task: {e}", exc_info=True)
            return {
                "status": "error",
                "task": task,
                "error": str(e),
                "environment_type": self.environment_type,
            }
        finally:
            self.environment_type = saved_env_type
