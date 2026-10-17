import sys
import os
import pytest
from unittest.mock import patch

# Ensure the script is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts')))

from benchmark_multiturn_memory import run_benchmark

@patch("benchmark_multiturn_memory.subprocess.Popen")
@patch("benchmark_multiturn_memory.wait_for_server")
@patch("benchmark_multiturn_memory.requests.post")
@patch("benchmark_multiturn_memory.psutil.Process")
def test_benchmark_multiturn_memory_local(mock_process, mock_post, mock_wait, mock_popen):
    mock_wait.return_value = True

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"response": "Mocked local response"}

    mock_proc_instance = mock_process.return_value
    mock_proc_instance.memory_info.return_value.rss = 50 * 1024 * 1024 # 50 MB

    peak_memory = run_benchmark(mode="local", turns=5)
    assert peak_memory >= 0

@patch("benchmark_multiturn_memory.requests.get")
@patch("benchmark_multiturn_memory.requests.post")
def test_benchmark_multiturn_memory_remote(mock_post, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.raise_for_status = lambda: None

    mock_post.return_value.status_code = 200
    mock_post.return_value.raise_for_status = lambda: None
    mock_post.return_value.json.return_value = {"response": "Mocked Remote Agent Response"}

    result = run_benchmark(mode="remote", turns=5)
    assert result == 1
