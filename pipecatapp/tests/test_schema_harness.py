import os
import json
import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from pipecatapp.tools.schema_harness_tool import SchemaHarnessTool, MockGridWorld
from pipecatapp.workflow.nodes.schema_nodes import HypothesizeNode, CertifyNode, PlanNode
from pipecatapp.workflow.context import WorkflowContext


class TestSchemaHarness:
    """Test suite for MockGridWorld, Schema Nodes, and SchemaHarnessTool."""

    def test_mock_grid_world_basic(self):
        """Verify the mock grid world behaves correctly with boundary collision."""
        env = MockGridWorld({"x": 0, "y": 0, "gx": 2, "gy": 2})
        assert env.get_state() == {"x": 0, "y": 0, "gx": 2, "gy": 2}
        assert not env.is_goal()

        # Move right
        assert env.step(3) == {"x": 1, "y": 0, "gx": 2, "gy": 2}
        # Move down
        assert env.step(1) == {"x": 1, "y": 1, "gx": 2, "gy": 2}
        # Move up (boundary check)
        env2 = MockGridWorld({"x": 0, "y": 0, "gx": 1, "gy": 1})
        assert env2.step(0) == {"x": 0, "y": 0, "gx": 1, "gy": 1}

    @pytest.mark.asyncio
    async def test_hypothesize_node(self):
        """Verify that HypothesizeNode generates correct world model code and notes."""
        node = HypothesizeNode({"id": "hypothesizer"})
        context = WorkflowContext({
            "nodes": [
                {
                    "id": "hypothesizer",
                    "inputs": [
                        {"name": "timeline", "connection": {"from_node": "Input", "from_output": "timeline"}},
                        {"name": "current_state", "connection": {"from_node": "Input", "from_output": "current_state"}},
                        {"name": "session_dir", "connection": {"from_node": "Input", "from_output": "session_dir"}},
                        {"name": "mismatch_info", "connection": {"from_node": "Certifier", "from_output": "mismatch_info"}}
                    ]
                }
            ]
        })

        # Inject inputs directly into outputs cache of the context
        context.node_outputs["Input"] = {
            "timeline": [],
            "current_state": {"x": 0, "y": 0, "gx": 1, "gy": 1},
            "session_dir": "/tmp/schema_harness_test_hypo/"
        }

        node.config = {
            "id": "hypothesizer",
            "inputs": [
                {"name": "timeline", "connection": {"from_node": "Input", "from_output": "timeline"}},
                {"name": "current_state", "connection": {"from_node": "Input", "from_output": "current_state"}},
                {"name": "session_dir", "connection": {"from_node": "Input", "from_output": "session_dir"}},
                {"name": "mismatch_info", "connection": {"from_node": "Certifier", "from_output": "mismatch_info"}}
            ]
        }

        await node.execute(context)

        # Check generated outputs
        code = context.node_outputs["hypothesizer"]["world_model_code"]
        notes = context.node_outputs["hypothesizer"]["notes"]

        assert "def step" in code
        assert "def is_goal" in code
        assert "Grid World" in notes

    @pytest.mark.asyncio
    @patch("pipecatapp.tools.code_runner_tool.CodeRunnerTool.run_python_code", new_callable=AsyncMock)
    async def test_certify_node(self, mock_run_python_code):
        """Verify that CertifyNode successfully validates a timeline and flags mismatches."""
        node = CertifyNode({"id": "certifier"})
        context = WorkflowContext({
            "nodes": [
                {
                    "id": "certifier",
                    "inputs": [
                        {"name": "timeline", "connection": {"from_node": "Input", "from_output": "timeline"}},
                        {"name": "world_model_code", "connection": {"from_node": "Hypothesizer", "from_output": "world_model_code"}},
                        {"name": "session_dir", "connection": {"from_node": "Input", "from_output": "session_dir"}}
                    ]
                }
            ]
        })

        # Inject inputs into Input node output
        context.node_outputs["Input"] = {
            "timeline": [
                {"state": {"x": 0, "y": 0, "gx": 2, "gy": 2}, "action": 3, "next_state": {"x": 1, "y": 0, "gx": 2, "gy": 2}},
                {"state": {"x": 1, "y": 0, "gx": 2, "gy": 2}, "action": 1, "next_state": {"x": 1, "y": 1, "gx": 2, "gy": 2}}
            ],
            "session_dir": "/tmp/schema_harness_test_certify/"
        }

        # Inject synthesized code into Hypothesizer node output
        world_model_code = (
            "def step(state, action):\n"
            "    x, y = state['x'], state['y']\n"
            "    gx, gy = state['gx'], state['gy']\n"
            "    if action == 1: y = min(9, y + 1)\n"
            "    elif action == 3: x = min(9, x + 1)\n"
            "    return {'x': x, 'y': y, 'gx': gx, 'gy': gy}\n\n"
            "def is_goal(state):\n"
            "    return state['x'] == state['gx'] and state['y'] == state['gy']\n"
        )
        context.node_outputs["Hypothesizer"] = {
            "world_model_code": world_model_code
        }

        node.config = {
            "id": "certifier",
            "inputs": [
                {"name": "timeline", "connection": {"from_node": "Input", "from_output": "timeline"}},
                {"name": "world_model_code", "connection": {"from_node": "Hypothesizer", "from_output": "world_model_code"}},
                {"name": "session_dir", "connection": {"from_node": "Input", "from_output": "session_dir"}}
            ]
        }

        mock_run_python_code.return_value = '{"status": "certified"}'

        await node.execute(context)

        is_certified = context.node_outputs["certifier"]["is_certified"]
        mismatch_info = context.node_outputs["certifier"]["mismatch_info"]

        assert is_certified is True
        assert mismatch_info is None

        # Test failure mismatch case by injecting an incorrect move in timeline
        context.node_outputs["Input"]["timeline"].append(
            {"state": {"x": 1, "y": 1, "gx": 2, "gy": 2}, "action": 1, "next_state": {"x": 9, "y": 9, "gx": 2, "gy": 2}}
        )

        mock_run_python_code.return_value = '{"status": "mismatch", "details": {"error": "Expected next state: ..."}}'

        await node.execute(context)

        is_certified = context.node_outputs["certifier"]["is_certified"]
        mismatch_info = context.node_outputs["certifier"]["mismatch_info"]

        assert is_certified is False
        assert "Mismatch" in mismatch_info

    @pytest.mark.asyncio
    @patch("pipecatapp.tools.code_runner_tool.CodeRunnerTool.run_python_code", new_callable=AsyncMock)
    async def test_plan_node(self, mock_run_python_code):
        """Verify that PlanNode finds a valid shortest path BFS route inside the sandbox."""
        node = PlanNode({"id": "planner"})
        context = WorkflowContext({
            "nodes": [
                {
                    "id": "planner",
                    "inputs": [
                        {"name": "current_state", "connection": {"from_node": "Input", "from_output": "current_state"}},
                        {"name": "world_model_code", "connection": {"from_node": "Hypothesizer", "from_output": "world_model_code"}},
                        {"name": "session_dir", "connection": {"from_node": "Input", "from_output": "session_dir"}},
                        {"name": "trigger", "connection": {"from_node": "Decider", "from_output": "output_true"}}
                    ]
                }
            ]
        })

        # Inject starting state
        context.node_outputs["Input"] = {
            "current_state": {"x": 0, "y": 0, "gx": 2, "gy": 2},
            "session_dir": "/tmp/schema_harness_test_plan/"
        }

        # Inject trigger from decider (True)
        context.node_outputs["Decider"] = {
            "output_true": True
        }

        # Inject synthesized code
        world_model_code = (
            "def step(state, action):\n"
            "    x, y = state['x'], state['y']\n"
            "    gx, gy = state['gx'], state['gy']\n"
            "    if action == 1: y = min(9, y + 1)\n"
            "    elif action == 3: x = min(9, x + 1)\n"
            "    return {'x': x, 'y': y, 'gx': gx, 'gy': gy}\n\n"
            "def is_goal(state):\n"
            "    return state['x'] == state['gx'] and state['y'] == state['gy']\n"
        )
        context.node_outputs["Hypothesizer"] = {
            "world_model_code": world_model_code
        }

        node.config = {
            "id": "planner",
            "inputs": [
                {"name": "current_state", "connection": {"from_node": "Input", "from_output": "current_state"}},
                {"name": "world_model_code", "connection": {"from_node": "Hypothesizer", "from_output": "world_model_code"}},
                {"name": "session_dir", "connection": {"from_node": "Input", "from_output": "session_dir"}},
                {"name": "trigger", "connection": {"from_node": "Decider", "from_output": "output_true"}}
            ]
        }

        mock_run_python_code.return_value = '{"plan": [1, 1, 3, 3]}'

        await node.execute(context)
        plan = context.node_outputs["planner"]["plan"]

        # To get from (0,0) to (2,2) with actions Down (1) and Right (3)
        # the shortest path is 1, 1, 3, 3 or 3, 3, 1, 1 (order doesn't matter, length 4)
        assert len(plan) == 4
        assert set(plan) == {1, 3}

    @pytest.mark.asyncio
    @patch("pipecatapp.tools.code_runner_tool.CodeRunnerTool.run_python_code", new_callable=AsyncMock)
    async def test_schema_harness_tool_end_to_end(self, mock_run_python_code):
        """Verify that SchemaHarnessTool runs the complete outer loop and clears levels."""
        tool = SchemaHarnessTool()
        session_id = "test-session-e2e"

        # Overwrite/reset files in the test session directory
        session_dir = f"/tmp/schema_harness_sessions/{session_id}/"
        timeline_path = os.path.join(session_dir, "timeline.jsonl")
        if os.path.exists(timeline_path):
            os.remove(timeline_path)

        def side_effect_func(*args, **kwargs):
            code = args[0]
            if "run_bfs(" in code:
                return '{"plan": [1, 3, 1, 3]}'

            # Prediction simulation for the inner loop
            if "prediction" in code or "pred = step(" in code:
                # We need to simulate the environment logic
                # It starts at (0, 0, 2, 2). The plan is [1, 3, 1, 3].
                # Down (1) increases y by 1. Right (3) increases x by 1.
                import json
                try:
                    state_str_start = code.find('step({') + 5
                    state_str_end = code.find('},') + 1
                    state = json.loads(code[state_str_start:state_str_end])

                    # Extract action safely
                    # e.g., pred = step({"x": 0, "y": 0, "gx": 2, "gy": 2}, 1)
                    action_str = code[state_str_end+1:code.find(')', state_str_end)].strip()
                    action = int(action_str)

                    if action == 1: state['y'] = min(9, state['y'] + 1)
                    if action == 3: state['x'] = min(9, state['x'] + 1)
                    return json.dumps({"prediction": state})
                except Exception as e:
                    return '{}'

            # The schema harness runs mock actions internally and then calls certify.
            # When the harness generates action 3 then 1, they take it to x:1 y:1.
            # We want to certify the actual expected behavior so the level clears.
            if "timeline_file" in code or "validation_script" in code or "status" in code:
                 return '{"status": "certified"}'

            return '{"status": "certified"}'

        mock_run_python_code.side_effect = side_effect_func

        report = await tool.run(
            session_id=session_id,
            environment_type="mock_grid_world",
            current_state={"x": 0, "y": 0, "gx": 2, "gy": 2}
        )

        assert "Success" in report
        assert "Total Actions Executed" in report
        assert "world_model.py" in report
        assert "notes.md" in report
