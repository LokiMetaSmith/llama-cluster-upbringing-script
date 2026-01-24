import pytest
import json
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from pipecatapp.tools.experiment_tool import ExperimentTool

@pytest.mark.asyncio
async def test_experiment_tool_flow():
    # Mock dependencies
    with patch("pipecatapp.tools.experiment_tool.SwarmTool") as MockSwarm, \
         patch("httpx.AsyncClient") as MockHttp, \
         patch("subprocess.run") as mock_subprocess, \
         patch("shutil.copytree") as mock_copytree, \
         patch("os.makedirs") as mock_makedirs, \
         patch("os.path.exists", return_value=True) as mock_exists, \
         patch("builtins.open", new_callable=MagicMock) as mock_open:

        # 1. Setup Swarm Mock
        mock_swarm_instance = MockSwarm.return_value
        # Return valid JSON with job IDs
        mock_swarm_instance.spawn_workers = AsyncMock(return_value=json.dumps({
            "job_ids": ["job-1", "job-2"],
            "message": "ok"
        }))

        # 2. Setup HTTP Mock (Event Bus)
        mock_client = AsyncMock()
        MockHttp.return_value.__aenter__.return_value = mock_client

        # Define side effects for GET /tasks/{id}
        # We need to simulate polling. First call returns empty, second returns results.

        # Result for Worker 1 (Fails)
        evt_w1 = {
            "kind": "worker_result",
            "content": json.dumps({
                "type": "solution_artifact",
                "file_path": "app.py",
                "content": "code_fails"
            }),
            "meta": {"task_id": "exp-w0"}
        }

        # Result for Worker 2 (Passes)
        evt_w2 = {
            "kind": "worker_result",
            "content": json.dumps({
                "type": "solution_artifact",
                "file_path": "app.py",
                "content": "code_passes"
            }),
            "meta": {"task_id": "exp-w1"}
        }

        # Mock responses
        # The tool calls GET /tasks/{id} for each task.
        # We can mock `get` to return different responses based on url
        async def mock_get(url):
            resp = MagicMock()
            resp.status_code = 200

            if "job-1" in url or "exp-w0" in url: # ID mapping depends on how tool generates IDs
                # The tool uses internal task IDs (exp-w0, exp-w1) to poll, not Swarm Job IDs directly?
                # Wait, tool generates `tasks` with IDs. Swarm returns Job IDs.
                # The tool polls based on `task["id"]`.
                # Let's see the tool code: `for task in tasks: t_id = task["id"] ... get(.../tasks/{t_id})`
                # So we expect URLs ending in generated IDs.
                resp.json.return_value = [evt_w1]
            elif "job-2" in url or "exp-w1" in url:
                resp.json.return_value = [evt_w2]
            else:
                resp.json.return_value = []
            return resp

        mock_client.get = AsyncMock(side_effect=mock_get)

        # 3. Setup Subprocess Mock (Test Evaluation)
        # We need it to fail for w1 code and pass for w2 code.
        # The tool writes the content to a file. We can't easily check file content here
        # because `open` is mocked. But we know the order of execution.
        # Or we can check `mock_open` calls?
        # Easier: Mock `subprocess.run` side effect based on some state or just sequence.
        # Sequence: Tool processes w1, then w2 (or order of dict iteration).

        # Let's ensure the tool processes results.
        # Since the loop runs `results = {}` then iterates `tasks`.
        # It processes w0 then w1.

        mock_subprocess_fail = MagicMock()
        mock_subprocess_fail.returncode = 1
        mock_subprocess_fail.stdout = "Tests Failed"
        mock_subprocess_fail.stderr = ""

        mock_subprocess_pass = MagicMock()
        mock_subprocess_pass.returncode = 0
        mock_subprocess_pass.stdout = "Tests Passed"
        mock_subprocess_pass.stderr = ""

        # The tool calls subprocess.run in _run_sandbox_eval
        # We can set side_effect to return fail then pass
        # But wait, results might come in any order if we had parallel polling,
        # but here it is serial inside the loop: `for t_id, evt in results.items()`
        # We will assume w0 (failed) is processed first if they arrive together.

        # To make it robust, we can inspect the file written? No, that's complex with mock_open.
        # Let's just assume sequence: Fail, Pass.
        mock_subprocess.side_effect = [mock_subprocess_fail, mock_subprocess_pass]

        # 4. Run Experiment
        tool = ExperimentTool(event_bus_url="http://mock:8000")

        # Fix UUID to have predictable task IDs?
        # The tool generates UUIDs. We can patch uuid.
        with patch("uuid.uuid4", return_value="exp"):
            # task IDs will be exp-w0, exp-w1
            # job IDs will be swarm-worker-exp-w0-exp (based on SwarmTool)

            # Update our mock_get logic to match these IDs
            result_json = await tool.run(
                task_description="Fix bug",
                test_command="pytest",
                num_workers=2,
                timeout_seconds=2
            )

        # 5. Assertions
        result = json.loads(result_json)

        assert result["total_workers"] == 2
        assert result["completed"] == 2

        # Winner should be the one that passed (w1/job-2)
        winner = result["winner"]
        assert winner is not None
        assert winner["passed"] is True
        assert "code_passes" in str(winner["artifact"])

        # Verify calls
        assert mock_copytree.called
        assert mock_subprocess.call_count == 2
