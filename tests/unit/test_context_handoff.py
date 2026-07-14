import sys
import os

# Append system package paths to ensure yaml is found even in strict clean-env runners
sys.path.append("/usr/lib/python3/dist-packages")

import tempfile
import pytest
import yaml
from unittest.mock import patch, MagicMock

# Append repository paths so we can import from pipecatapp
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(REPO_ROOT)
sys.path.append(os.path.join(REPO_ROOT, "pipecatapp"))
sys.path.append(os.path.join(REPO_ROOT, "pipecatapp", "tools"))

from pipecatapp.context_handoff import inject_context_handoff
from pipecatapp.workflow.runner import WorkflowRunner
from pipecatapp.workflow.context import WorkflowContext

def test_workflow_runner_extracts_global_mission_and_workflow_goal():
    # 1. Test with global_mission key
    yaml_content_1 = """
name: Test Mission Workflow 1
global_mission: "Build the #1 AI note-taking app to $1M MRR."
nodes:
  - id: input_node
    type: InputNode
    config:
      outputs:
        - name: user_text
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content_1)
        temp_path_1 = f.name

    try:
        runner = WorkflowRunner(temp_path_1)
        assert runner.global_mission == "Build the #1 AI note-taking app to $1M MRR."

        # Verify context also has the global_mission cascaded
        context = WorkflowContext(runner.workflow_definition)
        assert context.global_mission == "Build the #1 AI note-taking app to $1M MRR."
    finally:
        os.remove(temp_path_1)

    # 2. Test with workflow_goal key
    yaml_content_2 = """
name: Test Mission Workflow 2
workflow_goal: "Deploy high-availability database cluster."
nodes:
  - id: input_node
    type: InputNode
    config:
      outputs:
        - name: user_text
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content_2)
        temp_path_2 = f.name

    try:
        runner = WorkflowRunner(temp_path_2)
        assert runner.global_mission == "Deploy high-availability database cluster."

        # Verify context also has the global_mission cascaded
        context = WorkflowContext(runner.workflow_definition)
        assert context.global_mission == "Deploy high-availability database cluster."
    finally:
        os.remove(temp_path_2)

    # 3. Test with no keys (should be None)
    yaml_content_3 = """
name: Test Mission Workflow 3
nodes:
  - id: input_node
    type: InputNode
    config:
      outputs:
        - name: user_text
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content_3)
        temp_path_3 = f.name

    try:
        runner = WorkflowRunner(temp_path_3)
        assert runner.global_mission is None

        # Verify context also has global_mission as None
        context = WorkflowContext(runner.workflow_definition)
        assert context.global_mission is None
    finally:
        os.remove(temp_path_3)


def test_inject_context_handoff_with_goal_ancestry():
    messages = [
        {"role": "user", "content": "Let's begin the deployment."}
    ]
    new_expert = "postgres_technician"
    goal_lineage = "Build the #1 AI note-taking app to $1M MRR."

    with patch("pipecatapp.context_handoff.PolyphonyTool") as mock_polyphony_class:
        mock_instance = MagicMock()
        mock_polyphony_class.return_value = mock_instance

        updated_messages = inject_context_handoff(messages, new_expert, goal_lineage=goal_lineage)

        # 1. Verify PolyphonyTool called with correctly formatted prepended thought
        expected_thought = f"Goal Ancestry: {goal_lineage} | Swarm Context Handoff triggered. Active model switched to: {new_expert}"
        mock_instance.execute.assert_called_once_with("share", thought=expected_thought)

        # 2. Verify handoff prompt contains the prepended Goal Ancestry context
        assert len(updated_messages) == len(messages) + 1
        system_msg = updated_messages[0]
        assert system_msg["role"] == "system"
        assert f"Goal Ancestry (Contextual Lineage): {goal_lineage}" in system_msg["content"]
        assert "switching to postgres_technician" in system_msg["content"]
