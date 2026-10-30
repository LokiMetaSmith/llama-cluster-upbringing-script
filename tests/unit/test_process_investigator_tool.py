import pytest
from unittest.mock import patch, MagicMock
from pipecatapp.tools.process_investigator_tool import ProcessInvestigatorTool

@pytest.fixture
def tool():
    return ProcessInvestigatorTool()

def test_list_processes(tool):
    with patch.object(tool, "_run_cmd") as mock_run:
        mock_run.return_value = {
            "success": True,
            "exit_code": 0,
            "stdout": "USER PID %CPU %MEM ARGS\nuser1 1234 10.0 1.0 python app.py\n",
            "stderr": ""
        }
        res = tool.list_processes(sort_by="cpu", limit=5)
        assert "Top processes sorted by cpu" in res
        assert "user1 1234" in res

def test_py_spy_dump(tool):
    with patch("shutil.which", return_value="/usr/bin/py-spy"), \
         patch.object(tool, "_run_cmd") as mock_run:
        mock_run.return_value = {
            "success": True,
            "exit_code": 0,
            "stdout": "Thread 123 (idle)\n    main.py:10 - run",
            "stderr": ""
        }
        res = tool.py_spy(pid=1234, subaction="dump")
        assert "Thread 123" in res
        assert "main.py:10" in res

def test_py_spy_not_installed(tool):
    with patch("shutil.which", return_value=None), \
         patch("os.path.exists", return_value=False):
        res = tool.py_spy(pid=1234)
        assert "Error: 'py-spy' binary is not installed" in res

def test_gdb_py_bt(tool):
    with patch("shutil.which", return_value="/usr/bin/gdb"), \
         patch.object(tool, "_run_cmd") as mock_run:
        mock_run.return_value = {
            "success": True,
            "exit_code": 0,
            "stdout": "#0  0x0000 in PyEval_EvalFrameEx ()",
            "stderr": ""
        }
        res = tool.gdb_py_bt(pid=1234)
        assert "PyEval_EvalFrameEx" in res

def test_strace(tool):
    with patch("shutil.which", return_value="/usr/bin/strace"), \
         patch.object(tool, "_run_cmd") as mock_run:
        mock_run.return_value = {
            "success": True,
            "exit_code": 0,
            "stdout": "% time seconds usecs/call calls errors syscall\n",
            "stderr": "strace: Process 1234 attached\n"
        }
        res = tool.strace(pid=1234, duration=2)
        assert "strace output for PID 1234" in res
        assert "% time seconds" in res

def test_perf(tool):
    with patch("shutil.which", return_value="/usr/bin/perf"), \
         patch.object(tool, "_run_cmd") as mock_run:
        mock_run.return_value = {
            "success": True,
            "exit_code": 0,
            "stdout": " Performance counter stats for process id '1234':\n",
            "stderr": ""
        }
        res = tool.perf(pid=1234, mode="stat")
        assert "perf stat report for PID 1234" in res

def test_execute_dispatcher(tool):
    with patch.object(tool, "py_spy", return_value="mocked py_spy output"):
        res = tool.execute("py_spy", pid=1234, subaction="dump")
        assert res == "mocked py_spy output"
