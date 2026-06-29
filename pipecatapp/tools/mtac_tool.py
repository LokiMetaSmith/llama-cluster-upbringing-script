import logging
import json
import asyncio

# Dynamically import the pipeline orchestrator to prevent circular imports if it gets complex later
from pipecatapp.mtac_pipeline import MTACPipelineOrchestrator

logger = logging.getLogger(__name__)

class MTACTool:
    """
    A tool that allows the agent to orchestrate Model Training as Code (MTaC) runs.
    It can launch individual training stages or a full end-to-end training pipeline via the cluster orchestration.
    """

    def __init__(self):
        self.name = "mtac"
        self.description = (
            "Launch Model Training as Code (MTaC) jobs on the cluster. "
            "Allows you to run specific model training stages like 'sft' (Supervised Fine Tuning), "
            "'rl' (Reinforcement Learning), 'eval' (Evaluation), or a 'full_pipeline'. "
            "Pass a JSON configuration string for the given stage."
        )
        self.input_schema = {
            "type": "object",
            "properties": {
                "stage": {
                    "type": "string",
                    "description": "The pipeline stage to run. Supported values: 'sft', 'rl', 'eval', or 'full_pipeline'."
                },
                "config": {
                    "type": "string",
                    "description": "A JSON string representing the configuration for the chosen stage. Example: '{\"learning_rate\": 1e-4}'."
                }
            },
            "required": ["stage"]
        }
        self.orchestrator = MTACPipelineOrchestrator()

    async def run(self, stage: str, config: str = "{}") -> str:
        """
        Executes the requested MTaC pipeline stage.
        """
        try:
            parsed_config = json.loads(config)
        except json.JSONDecodeError:
            return "Error: Invalid JSON string provided for the `config` argument."

        supported_stages = ["sft", "rl", "eval", "full_pipeline"]
        if stage not in supported_stages:
            return f"Error: Unsupported stage '{stage}'. Must be one of {supported_stages}."

        logger.info(f"Agent triggered MTaC tool for stage '{stage}' with config: {parsed_config}")

        try:
            if stage == "full_pipeline":
                result = await self.orchestrator.run_full_pipeline(parsed_config)
            else:
                result = await self.orchestrator.run_stage(stage, parsed_config)

            return f"MTaC execution complete.\nResult:\n{json.dumps(result, indent=2)}"
        except Exception as e:
            logger.error(f"MTaC tool execution failed: {e}")
            return f"Error during MTaC execution: {str(e)}"
