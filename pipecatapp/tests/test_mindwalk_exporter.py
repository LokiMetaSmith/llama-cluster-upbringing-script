import os
import json
import tempfile
import pytest
from pipecatapp.utils.mindwalk_exporter import MindwalkTraceExporter


def test_export_trace_basic():
    exporter = MindwalkTraceExporter()
    session_id = "test-session-123"
    harness = "pipecatapp-test"

    events = [
        {
            "ts": "2026-07-11T12:00:00Z",
            "tool": "search_tool",
            "action": "search",
            "isError": False,
            "resultBytes": 100,
            "targets": [{"path": "src/main.py", "touch": "hit"}]
        },
        {
            "ts": "2026-07-11T12:01:00Z",
            "tool": "file_editor",
            "action": "edit",
            "isError": False,
            "resultBytes": 200,
            "targets": [{"path": "src/main.py", "touch": "edit"}]
        }
    ]

    marks = [
        {"type": "user-message", "note": "Start processing"},
        {"type": "compaction", "note": "Compact history"}
    ]

    trace = exporter.export_trace(
        session_id=session_id,
        harness=harness,
        events=events,
        marks=marks,
        model="gpt-4",
        cwd="/workspace",
        files_in_repo=42
    )

    # Validate Top level fields
    assert trace["version"] == 1
    assert "session" in trace
    assert "events" in trace
    assert "marks" in trace
    assert "stats" in trace

    # Validate Session block
    session = trace["session"]
    assert session["id"] == session_id
    assert session["harness"] == harness
    assert session["model"] == "gpt-4"
    assert session["cwd"] == "/workspace"
    assert session["eventCount"] == 2

    # Validate Event sequence normalization
    assert trace["events"][0]["seq"] == 0
    assert trace["events"][1]["seq"] == 1

    # Validate Mark sequence normalization
    assert trace["marks"][0]["seq"] == 0
    assert trace["marks"][1]["seq"] == 1

    # Validate Stats Block
    stats = trace["stats"]
    assert stats["filesInRepo"] == 42
    assert stats["edited"] == 1
    assert stats["fovea"] == 1       # src/main.py was edited (which puts it in fovea)
    assert stats["parafovea"] == 0   # src/main.py was hit first, but eventually edited (so fovea wins)
    assert stats["eventsBeforeFirstEdit"] == 1  # 1 event (the search) before the edit event
    assert stats["userTurns"] == 1
    assert stats["compactions"] == 1
    assert stats["subagents"] == 0
    assert stats["resultBytes"] == 300
    assert stats["errorRate"] == 0.0


def test_stats_churn_and_verify():
    exporter = MindwalkTraceExporter()

    events = [
        {
            "action": "edit",
            "targets": [{"path": "src/helper.py", "touch": "edit"}],
            "resultBytes": 50
        },
        {
            "action": "verify",
            "isError": True
        },
        {
            "action": "edit",
            "targets": [{"path": "src/helper.py", "touch": "edit"}],
            "resultBytes": 50
        },
        {
            "action": "edit",
            "targets": [{"path": "src/helper.py", "touch": "edit"}],
            "resultBytes": 50
        },
        {
            "action": "verify",
            "isError": False
        },
        {
            "action": "edit",
            "targets": [{"path": "src/main.py", "touch": "edit"}],
            "resultBytes": 20
        }
    ]

    trace = exporter.export_trace(
        session_id="test-churn",
        harness="pytest",
        events=events,
        marks=[]
    )

    stats = trace["stats"]

    # Verify action counts
    assert stats["actions"]["edit"] == 4
    assert stats["actions"]["verify"] == 2

    # Verify error counts
    assert stats["errors"]["verify"] == 1

    # Verify regression rate and error rate
    assert stats["regressionRate"] == 0.5  # 1 error / 2 verifies
    assert stats["errorRate"] == 1 / 6.0  # 1 error / 6 total actions

    # Max edits per file: src/helper.py has 3 edits, src/main.py has 1 edit
    assert stats["maxEditsPerFile"] == 3

    # Churn files: helper.py was edited 3 times (>=3), main.py 1 time (<3). Total = 1.
    assert stats["churnFiles"] == 1

    # Edits after last verify: last verify is at index 4. The edit at index 5 is after it.
    assert stats["editsAfterLastVerify"] == 1


def test_export_to_file():
    exporter = MindwalkTraceExporter()

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "trace.json")
        exporter.export_trace_to_file(
            filepath=filepath,
            session_id="session-file",
            harness="pytest",
            events=[{"action": "search"}],
            marks=[]
        )

        assert os.path.exists(filepath)
        with open(filepath, "r") as f:
            data = json.load(f)

        assert data["session"]["id"] == "session-file"
        assert data["stats"]["actions"]["search"] == 1
