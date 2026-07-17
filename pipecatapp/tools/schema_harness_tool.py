import os
import json
import uuid
import logging
from typing import Dict, Any, List, Optional
from pipecatapp.tools.code_runner_tool import CodeRunnerTool

logger = logging.getLogger(__name__)

class SchemaHarnessTool:
    """
    SchemaHarnessTool coordinates the outer "observe -> deliberate -> execute -> record"
    loop against an environment using specialized workflows. It manages session directories,
    records the transition Timeline, performs step-by-step prediction checking in the sandbox,
    and terminates/re-plans on surprise mismatches.
    """
    def __init__(self):
        self.name = "schema_harness"
        self.description = (
            "Runs the Schema Harness loop against a target environment (e.g., mock_grid_world) "
            "to discover mechanisms, synthesize world models, backtest them, and execute plan actions safely."
        )
        self.input_schema = {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Unique session identifier. If not provided, a new one is generated."
                },
                "environment_type": {
                    "type": "string",
                    "description": "Type of environment, e.g., 'mock_grid_world'.",
                    "default": "mock_grid_world"
                },
                "current_state": {
                    "type": "object",
                    "description": "Optional starting state overrides."
                }
            },
            "required": []
        }

    async def run(self, session_id: Optional[str] = None, environment_type: str = "mock_grid_world", current_state: Optional[Dict[str, Any]] = None) -> str:
        """Executes the tool logic."""
        if not session_id:
            session_id = str(uuid.uuid4())

        session_dir = f"/tmp/schema_harness_sessions/{session_id}/"
        os.makedirs(session_dir, exist_ok=True)

        timeline_path = os.path.join(session_dir, "timeline.jsonl")

        # Initialize environment
        env = None
        if environment_type == "mock_grid_world":
            env = MockGridWorld(current_state)
        else:
            return f"Error: Unsupported environment type '{environment_type}'."

        # Load existing timeline if any
        timeline = []
        if os.path.exists(timeline_path):
            with open(timeline_path, "r") as f:
                for line in f:
                    if line.strip():
                        timeline.append(json.loads(line.strip()))

        # If timeline is empty, take some initial exploratory actions to gather data for synthesis
        if not timeline:
            logger.info("SchemaHarness: Timeline is empty. Running initial exploration phase.")
            exploratory_actions = [1, 3] # e.g., Down, Right
            for act in exploratory_actions:
                state_before = env.get_state()
                state_after = env.step(act)
                trans = {
                    "state": state_before,
                    "action": act,
                    "next_state": state_after
                }
                timeline.append(trans)
                # Write to timeline file
                with open(timeline_path, "a") as f:
                    f.write(json.dumps(trans) + "\n")

        # Execute the outer loop (Observe -> Deliberate -> Execute -> Record)
        max_outer_iterations = 5
        actions_executed = []
        final_status = "Failed"
        mismatches_encountered = 0
        last_world_model_code = ""
        last_notes = ""

        for iteration in range(max_outer_iterations):
            state = env.get_state()
            if env.is_goal():
                final_status = "Success"
                break

            logger.info(f"SchemaHarness: Iteration {iteration}. Current state: {state}")

            # Deliberate & Plan: run the specialized schema harness workflow
            from pipecatapp.workflow.runner import WorkflowRunner
            workflow_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "workflows", "schema_harness_workflow.yaml")
            runner = WorkflowRunner(workflow_path)

            global_inputs = {
                "timeline": timeline,
                "current_state": state,
                "session_dir": session_dir
            }

            try:
                outputs = await runner.run(global_inputs) or {}
            except Exception as e:
                logger.error(f"SchemaHarness workflow run failed: {e}")
                return f"SchemaHarness Failure: Workflow runner failed: {e}"

            plan = outputs.get("plan") or []
            last_world_model_code = outputs.get("world_model_code") or ""
            last_notes = outputs.get("notes") or ""

            logger.info(f"SchemaHarness: Workflow generated plan: {plan}")

            if not plan:
                logger.warning("SchemaHarness: No valid plan generated. Taking random action to explore.")
                # Fallback exploratory action
                exploratory_action = 1 # Move down
                state_before = env.get_state()
                state_after = env.step(exploratory_action)
                trans = {
                    "state": state_before,
                    "action": exploratory_action,
                    "next_state": state_after
                }
                timeline.append(trans)
                with open(timeline_path, "a") as f:
                    f.write(json.dumps(trans) + "\n")
                actions_executed.append(exploratory_action)
                continue

            # Execute plan with step-by-step prediction checking in the sandbox
            plan_voided = False
            for act in plan:
                state_before = env.get_state()

                # Check prediction safely using CodeRunnerTool in the sandbox
                predicted_state = await self._predict_next_state(last_world_model_code, state_before, act)

                # Take action in environment
                actual_state = env.step(act)
                actions_executed.append(act)

                # Record transition
                trans = {
                    "state": state_before,
                    "action": act,
                    "next_state": actual_state
                }
                timeline.append(trans)
                with open(timeline_path, "a") as f:
                    f.write(json.dumps(trans) + "\n")

                # Prediction Check
                if actual_state != predicted_state:
                    logger.warning(f"SchemaHarness: Mismatch detected! Expected {predicted_state}, got {actual_state}.")
                    mismatches_encountered += 1
                    plan_voided = True
                    break # Void the rest of the plan and return to deliberation (the outer loop)

                if env.is_goal():
                    break

            if plan_voided:
                logger.info("SchemaHarness: Plan voided due to prediction surprise. Re-planning...")
                continue

            if env.is_goal():
                final_status = "Success"
                break

        # Generate markdown report
        report = []
        report.append("# Schema Harness Execution Report")
        report.append(f"**Session ID:** `{session_id}`")
        report.append(f"**Status:** `{final_status}`")
        report.append(f"**Total Actions Executed:** {len(actions_executed)} (Plan steps: `{actions_executed}`)")
        report.append(f"**Prediction Surprises / Mismatches:** {mismatches_encountered}")
        report.append(f"**Timeline Record Size:** {len(timeline)}")
        report.append("")
        report.append("## Synthesized Notes (`notes.md`)")
        report.append(last_notes or "*None*")
        report.append("")
        report.append("## Certified World Model (`world_model.py`)")
        report.append(f"```python\n{last_world_model_code}\n```")

        return "\n".join(report)

    async def _predict_next_state(self, world_model_code: str, state: Dict[str, Any], action: Any) -> Dict[str, Any]:
        """Runs the step function inside the sandbox to calculate the predicted next state."""
        script = f"""
{world_model_code}

import json
try:
    pred = step({json.dumps(state)}, {json.dumps(action)})
    print(json.dumps({{"prediction": pred}}))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
"""
        code_runner = CodeRunnerTool()
        try:
            output = await code_runner.run_python_code(script)
            start_idx = output.find('{')
            end_idx = output.rfind('}')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = output[start_idx:end_idx+1]
                res_data = json.loads(json_str)
                return res_data.get("prediction") or {}
        except Exception as e:
            logger.error(f"Prediction check sandbox failed: {e}")
        return {}


class MockGridWorld:
    """A simplified 10x10 Grid World environment with basic collision and a static goal."""
    def __init__(self, current_state: Optional[Dict[str, Any]] = None):
        if current_state:
            self.x = current_state.get("x", 0)
            self.y = current_state.get("y", 0)
            self.gx = current_state.get("gx", 9)
            self.gy = current_state.get("gy", 9)
        else:
            self.x = 0
            self.y = 0
            self.gx = 9
            self.gy = 9

    def get_state(self) -> Dict[str, Any]:
        return {"x": self.x, "y": self.y, "gx": self.gx, "gy": self.gy}

    def is_goal(self) -> bool:
        return self.x == self.gx and self.y == self.gy

    def step(self, action: int) -> Dict[str, Any]:
        # 0: Up, 1: Down, 2: Left, 3: Right
        if action == 0:
            self.y = max(0, self.y - 1)
        elif action == 1:
            self.y = min(9, self.y + 1)
        elif action == 2:
            self.x = max(0, self.x - 1)
        elif action == 3:
            self.x = min(9, self.x + 1)
        return self.get_state()
