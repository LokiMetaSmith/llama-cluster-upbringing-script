import pytest
import os
import asyncio
import tempfile
from pipecatapp.memory_backends_impl.pmm_backend import PMMMemoryBackend
from pipecatapp.tools.memory_candidate_tool import MemoryCandidateTool

@pytest.fixture
def temp_db():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "pmm_test.db")
        backend = PMMMemoryBackend(db_path=db_path)
        tool = MemoryCandidateTool(backend=backend)
        yield tool, backend

def test_memory_candidate_schema(temp_db):
    tool, _ = temp_db
    schema = tool.get_schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "memory_candidate"
    assert "emit" in schema["function"]["parameters"]["properties"]["action"]["enum"]

def test_candidate_lifecycle(temp_db):
    tool, backend = temp_db

    # 1. Emit candidate
    res = asyncio.run(tool.execute(
        action="emit",
        candidate_text="Always use strict typing in Python workflow nodes.",
        source="subagent-coder",
        session_id="session-101",
        category="convention",
        importance=4
    ))
    assert "Successfully emitted memory candidate (ID: 1)" in res

    # 2. List pending
    list_res = asyncio.run(tool.execute(action="list_pending", session_id="session-101"))
    assert "Always use strict typing in Python workflow nodes." in list_res
    assert "[1] Session: session-101" in list_res

    # 3. Promote candidate
    promote_res = asyncio.run(tool.execute(action="promote", candidate_id=1))
    assert "Successfully promoted candidate ID 1 to durable memory" in promote_res

    # 4. Verify in durable memory
    memories = backend.get_unconsolidated_memories()
    assert len(memories) >= 1
    assert "Always use strict typing in Python workflow nodes." in memories[0]["raw_text"]

    # 5. List pending should now be empty
    list_after = asyncio.run(tool.execute(action="list_pending", session_id="session-101"))
    assert "No pending memory candidates found." in list_after

def test_candidate_rejection(temp_db):
    tool, _ = temp_db

    # Emit candidate
    asyncio.run(tool.execute(
        action="emit",
        candidate_text="Temporary debug note.",
        source="subagent-explore",
        session_id="session-102"
    ))

    # Reject candidate
    reject_res = asyncio.run(tool.execute(action="reject", candidate_id=1))
    assert "Successfully rejected candidate ID 1." in reject_res

    # List pending should be empty
    list_res = asyncio.run(tool.execute(action="list_pending", session_id="session-102"))
    assert "No pending memory candidates found." in list_res
