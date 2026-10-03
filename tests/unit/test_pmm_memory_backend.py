import os
import pytest
from pipecatapp.memory import MemoryStore, Document
from pipecatapp.memory_backends_impl.pmm_backend import PMMMemoryBackend

@pytest.fixture
def temp_pmm_db(tmp_path):
    return str(tmp_path / "test_pmm.db")

def test_pmm_memory_backend_direct(temp_pmm_db):
    backend = PMMMemoryBackend(db_path=temp_pmm_db)

    # Test text event add and search
    backend.add("Antigravity cognitive architecture")
    backend.add("Distributed consensus on legacy hardware")
    results = backend.search("Antigravity")
    assert len(results) == 1
    assert "Antigravity cognitive architecture" in results[0]

    # Test structured memory
    mem_id = backend.add_memory(
        source="conversation",
        raw_text="The cluster has 3 nodes.",
        summary="Cluster node count",
        entities=["cluster", "nodes"],
        topics=["hardware", "topology"],
        importance=8,
        metadata={"region": "local"}
    )
    assert mem_id > 0

    mem = backend.get_memory(mem_id)
    assert mem is not None
    assert mem["source"] == "conversation"
    assert mem["raw_text"] == "The cluster has 3 nodes."
    assert mem["consolidated"] is False

    unconsolidated = backend.get_unconsolidated_memories()
    assert len(unconsolidated) >= 1
    assert any(m["id"] == mem_id for m in unconsolidated)

    # Test consolidation
    cons_id = backend.add_consolidation([mem_id], "Summary of cluster", "Nodes are functioning")
    assert cons_id > 0
    cons = backend.get_consolidation(cons_id)
    assert cons is not None
    assert cons["summary"] == "Summary of cluster"

    # Mark consolidated
    backend.mark_memory_consolidated(mem_id)
    updated_mem = backend.get_memory(mem_id)
    assert updated_mem["consolidated"] is True

    # Test activities
    act_id = backend.add_activity("tool_call", "Invoked RAG tool", {"tool": "rag"})
    assert act_id > 0
    acts = backend.get_activities(10)
    assert len(acts) >= 1
    assert acts[0]["activity_type"] == "tool_call"

    # Test dynamic skills
    backend.save_skill("deploy_check", "Check cluster deployment health", "def check(): return True")
    skill = backend.get_skill("deploy_check")
    assert skill is not None
    assert skill["description"] == "Check cluster deployment health"

    skills = backend.list_skills()
    assert len(skills) == 1

    deleted = backend.delete_skill("deploy_check")
    assert deleted is True
    assert backend.get_skill("deploy_check") is None

    # Test Haystack documents
    docs = [
        Document(id="doc-1", content="Cluster runbook", metadata={"source": "docs", "tier": "p0"}),
        Document(id="doc-2", content="Troubleshooting guide", metadata={"source": "docs", "tier": "p1"}),
    ]
    written = backend.write_documents(docs)
    assert written == 2

    filtered = backend.filter_documents({"source": "docs"})
    assert len(filtered) >= 2

def test_memory_store_with_pmm_env(temp_pmm_db, monkeypatch):
    monkeypatch.setenv("USE_PMM_MEMORY", "true")
    store = MemoryStore(sqlite_file=temp_pmm_db)
    assert isinstance(store.backend, PMMMemoryBackend)

    store.add("Persistent Mind Model is active")
    results = store.search("Persistent Mind Model")
    assert len(results) == 1
