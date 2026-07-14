import os
import sys
import json
import shutil
import tempfile
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch

# Ensure absolute package imports work across un-bootstrapped environments
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "pipecatapp")))

from pipecatapp.utils.ansible_triage import AnsibleTriageHandler
from pipecatapp.tools.ansible_exception_handler_tool import AnsibleExceptionHandlerTool

@pytest.fixture
def temp_context_dir():
    """Creates a temporary failure context directory populated with sample files."""
    temp_dir = tempfile.mkdtemp()

    # 1. failure_log.txt
    with open(os.path.join(temp_dir, "failure_log.txt"), "w") as f:
        f.write("nginx: [emerg] 'proxy_pass' cannot have URI part in app.conf.j2 task Ensure configuration is valid")

    # 2. failing_task.yml
    with open(os.path.join(temp_dir, "failing_task.yml"), "w") as f:
        f.write("- name: Ensure Nginx configuration is valid\n  ansible.builtin.template:\n    src: app.conf.j2\n    dest: /etc/nginx/conf.d/app.conf")

    # 3. host_vars.json
    with open(os.path.join(temp_dir, "host_vars.json"), "w") as f:
        json.dump({"api_version": "v2", "nginx_port": 8080}, f)

    # 4. rendered_artifacts
    artifacts_dir = os.path.join(temp_dir, "rendered_artifacts")
    os.makedirs(artifacts_dir)
    with open(os.path.join(artifacts_dir, "app.conf.j2"), "w") as f:
        f.write("proxy_pass http://upstream_server/api/v1/;")

    yield temp_dir

    # Clean up
    shutil.rmtree(temp_dir)

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
@patch("subprocess.run")
@patch("os.path.exists", return_value=True)
async def test_ansible_triage_success(mock_exists, mock_run, mock_post, temp_context_dir):
    """Tests the full successful triage loop including LLM call, reverse compilation, and Git/Opengist push."""
    # Mock LLM API response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "root_cause": "Trailing slash mismatch in proxy_pass directive under api_version v2.",
                    "changes": [{
                        "filepath": "ansible/roles/nginx/templates/app.conf.j2",
                        "search_content": "proxy_pass http://upstream_server/api/v1/;",
                        "replace_content": "proxy_pass http://upstream_server/api/{{ api_version }};"
                    }],
                    "target_port": 8080,
                    "health_check_command": "curl -f http://localhost:8080"
                })
            }
        }]
    }
    mock_post.return_value = mock_resp

    # Mock subprocess.run for git/linter/health-check commands
    mock_proc = MagicMock()
    mock_proc.returncode = 0
    mock_proc.stdout = "Command execution simulation successful"
    mock_proc.stderr = ""
    mock_run.return_value = mock_proc

    # Instantiate handler
    handler = AnsibleTriageHandler(context_dir=temp_context_dir, task_id="nginx-config-error")

    # Patch self-hosted endpoint lookup & file modification
    with patch.dict(os.environ, {"LOCAL_LLM_URL": "http://localhost:8000"}):
        with patch("builtins.open", mock_open_file_context()):
            with patch("socket.create_connection") as mock_conn:
                result = await handler.run_triage()

                # Assertions
                assert result["status"] == "SUCCESS"
                assert "Trailing slash mismatch" in result["root_cause"]
                assert "ansible/roles/nginx/templates/app.conf.j2" in result["applied_files"]
                assert result["verification_status"] == "SUCCESS"
                assert "pr_summary_path" in result

def mock_open_file_context():
    """Helper to mock file reading/writing safely within the handler."""
    file_contents = {
        "ansible/roles/nginx/templates/app.conf.j2": "proxy_pass http://upstream_server/api/v1/;",
        os.path.join("/app", "pull_request_summary.md"): ""
    }

    original_open = open
    def custom_open(file, mode="r", *args, **kwargs):
        # Resolve path
        path_str = str(file)
        for key in file_contents:
            if key in path_str:
                mock_file = MagicMock()
                if "r" in mode:
                    mock_file.read.return_value = file_contents[key]
                elif "w" in mode:
                    def write_side_effect(data):
                        file_contents[key] = data
                        return len(data)
                    mock_file.write.side_effect = write_side_effect

                # Context manager support
                mock_file.__enter__.return_value = mock_file
                return mock_file
        return original_open(file, mode, *args, **kwargs)

    return custom_open

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
@patch("subprocess.run")
async def test_ansible_triage_offline_fallback(mock_run, mock_post, temp_context_dir):
    """Tests that the handler gracefully falls back to creating local Git bundle and PR file if Opengist is offline."""
    # Mock LLM API response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "root_cause": "A syntax issue in playbook.yaml",
                    "changes": [],
                    "target_port": None,
                    "health_check_command": None
                })
            }
        }]
    }
    mock_post.return_value = mock_resp

    # Mock subprocess.run:
    # 1. syntax check (0)
    # 2. dry run (0)
    # 3. git branch checkout (0)
    # 4. git add (0)
    # 5. git commit (0)
    # 6. git remote push to opengist (fails with 1 - simulating offline/unreachable)
    # 7. git bundle create (0)
    def side_effect(cmd, *args, **kwargs):
        proc = MagicMock()
        if "push" in cmd:
            proc.returncode = 1
            proc.stderr = "Could not resolve host opengist-http.service.consul"
        else:
            proc.returncode = 0
            proc.stdout = "Git command mock successful"
        return proc

    mock_run.side_effect = side_effect

    # Instantiate handler
    handler = AnsibleTriageHandler(context_dir=temp_context_dir, task_id="offline-fall")

    with patch.dict(os.environ, {"LOCAL_LLM_URL": "http://localhost:8000"}):
        # Mock git operations
        with patch("builtins.open", mock_open_file_context()):
            result = await handler.run_triage()

            # Assertions
            assert result["status"] == "SUCCESS"
            assert "bundle_path" in result
            assert "pr_summary_path" in result
            assert "pushed_url" not in result

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
async def test_ansible_triage_llm_timeout(mock_post, temp_context_dir):
    """Tests that the handler fails cleanly when the local/remote LLM is down/unreachable or times out."""
    # Simulate timeout/connection failure
    mock_post.side_effect = TimeoutError("Connection to LLM host timed out.")

    handler = AnsibleTriageHandler(context_dir=temp_context_dir, task_id="timeout-fail")

    with patch.dict(os.environ, {"LOCAL_LLM_URL": "http://localhost:8000"}):
        with pytest.raises(TimeoutError) as exc_info:
            await handler.run_triage()

        assert "LLM API call failed or timed out" in str(exc_info.value)

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post")
@patch("subprocess.run")
async def test_ansible_exception_handler_tool(mock_run, mock_post, temp_context_dir):
    """Tests the AnsibleExceptionHandlerTool wrapper integration."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "root_cause": "A sample root cause.",
                    "changes": [],
                    "target_port": None,
                    "health_check_command": None
                })
            }
        }]
    }
    mock_post.return_value = mock_resp

    mock_proc = MagicMock()
    mock_proc.returncode = 0
    mock_run.return_value = mock_proc

    tool = AnsibleExceptionHandlerTool()
    assert tool.name == "ansible_exception_handler"

    with patch.dict(os.environ, {"LOCAL_LLM_URL": "http://localhost:8000"}):
        with patch("builtins.open", mock_open_file_context()):
            result_str = await tool.run(context_dir=temp_context_dir, task_id="tool-test")
            assert "Triage status: SUCCESS" in result_str
            assert "Applied Upstream Fixes" in result_str
            assert "Verification Check: SUCCESS" in result_str
