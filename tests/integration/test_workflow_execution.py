import os
import pytest
import yaml
from pipecatapp.workflow.runner import WorkflowRunner

@pytest.mark.asyncio
async def test_durable_git_coordination_loop_integration(tmp_path, mocker):
    # Mock SentenceTransformer to prevent local embedding model file lookup error
    mock_st = mocker.MagicMock()
    mock_st.encode.return_value = [0.1] * 384
    mock_st.get_sentence_embedding_dimension.return_value = 384
    mocker.patch("pipecatapp.memory_legacy.SentenceTransformer", return_value=mock_st)

    # Mock Consul service discovery and Polyphony subprocess calls
    mock_subproc = mocker.MagicMock()
    mock_subproc.returncode = 0
    mock_subproc.stdout = "Task claimed successfully"
    mocker.patch("subprocess.run", return_value=mock_subproc)

    # Set root dir context
    root_dir = str(tmp_path)
    test_file = str(tmp_path / "sample_code.py")
    with open(test_file, "w") as f:
        f.write("def compute(x):\n    if x > 0:\n        return x * 2\n    return 0\n")

    workflow_path = "workflows/durable_git_coordination_loop.yaml"
    assert os.path.exists(workflow_path)

    with open(workflow_path, "r") as f:
        wf_def = yaml.safe_load(f)

    runner = WorkflowRunner(workflow_path=workflow_path)
    initial_inputs = {"target_file": test_file}

    await runner.run(global_inputs=initial_inputs)

    assert runner.context is not None
    print("NODE OUTPUTS:", runner.context.node_outputs)
    assert "init_git_plan" in runner.context.node_outputs
    assert "log_evidence" in runner.context.node_outputs
    # Check that durable Git artifacts were created in .liminal/projects/
    project_dir = os.path.join(".liminal", "projects", "swarm_task_001")
    assert os.path.exists(os.path.join(project_dir, "PLAN.md"))
    assert os.path.exists(os.path.join(project_dir, "EVIDENCE.md"))

    # Cleanup created project test files
    if os.path.exists(project_dir):
        import shutil
        shutil.rmtree(os.path.dirname(project_dir), ignore_errors=True)
