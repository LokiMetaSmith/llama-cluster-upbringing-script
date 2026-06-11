import pytest
import os
import json
from unittest.mock import patch, MagicMock
from pipecatapp.memory import MemoryStore

@pytest.fixture
def memory_instance_advanced(tmp_path):
    mem_dir = tmp_path / "memory_advanced"
    mem_dir.mkdir()
    with patch("pipecatapp.memory.faiss") as mock_faiss, \
         patch("pipecatapp.memory.SentenceTransformer"):
        mock_faiss.IndexFlatL2.return_value = MagicMock()
        mock_faiss.read_index.return_value = MagicMock()
        memory = MemoryStore(
            index_file=str(mem_dir / "index_adv.faiss"),
            store_file=str(mem_dir / "store_adv.json"),
            sqlite_file=str(mem_dir / "db_adv.sqlite")
        )
        return memory

def test_get_memory_adv(memory_instance_advanced):
    memory_id = memory_instance_advanced.add_memory(
        source="test_source",
        raw_text="This is a test memory",
        metadata={"key": "value"}
    )
    retrieved = memory_instance_advanced.get_memory(memory_id)
    assert retrieved is not None
    assert retrieved["source"] == "test_source"
    assert retrieved["raw_text"] == "This is a test memory"
    assert retrieved["metadata"]["key"] == "value"

def test_get_memory_not_found_adv(memory_instance_advanced):
    retrieved = memory_instance_advanced.get_memory(999)
    assert retrieved is None

def test_get_consolidation_adv(memory_instance_advanced):
    cursor = memory_instance_advanced.conn.cursor()
    cursor.execute('''
        INSERT INTO consolidations (source_ids, summary, insight)
        VALUES (?, ?, ?)
    ''', (
        json.dumps([1, 2]),
        memory_instance_advanced._encrypt("Test summary"),
        memory_instance_advanced._encrypt("Test insight")
    ))
    memory_instance_advanced.conn.commit()
    consolidation_id = cursor.lastrowid
    retrieved = memory_instance_advanced.get_consolidation(consolidation_id)
    assert retrieved is not None
    assert retrieved["source_ids"] == [1, 2]
    assert retrieved["summary"] == "Test summary"
    assert retrieved["insight"] == "Test insight"

def test_get_consolidation_not_found_adv(memory_instance_advanced):
    retrieved = memory_instance_advanced.get_consolidation(999)
    assert retrieved is None

def test_add_and_get_activities_adv(memory_instance_advanced):
    id1 = memory_instance_advanced.add_activity("spawn", "Agent spawned", {"agent_id": "123"})
    id2 = memory_instance_advanced.add_activity("tool", "Tool used", {"tool_name": "search"})
    activities = memory_instance_advanced.get_activities(limit=10)
    assert len(activities) == 2
    assert activities[0]["activity_type"] == "tool"
    assert activities[1]["activity_type"] == "spawn"

def test_filter_documents_adv(memory_instance_advanced):
    memory_instance_advanced.add_memory(source="source_A", raw_text="Document 1", doc_id="doc-1")
    memory_instance_advanced.add_memory(source="source_B", raw_text="Document 2", doc_id="doc-2")
    memory_instance_advanced.add_memory(source="source_A", raw_text="Document 3", doc_id="doc-3")
    docs = memory_instance_advanced.filter_documents({"source": "source_A"})
    assert len(docs) == 2
    doc_ids = [doc.id for doc in docs]
    assert "doc-1" in doc_ids
    assert "doc-3" in doc_ids

def test_filter_documents_empty_filters_adv(memory_instance_advanced):
    memory_instance_advanced.add_memory(source="source_A", raw_text="Document 1")
    docs = memory_instance_advanced.filter_documents()
    assert docs == []
