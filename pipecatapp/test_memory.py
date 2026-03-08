import pytest
from unittest.mock import MagicMock, patch, mock_open
import numpy as np
import json

from memory import MemoryStore

@pytest.fixture
def mock_sentence_transformer():
    """Fixture to mock the SentenceTransformer."""
    with patch('memory.SentenceTransformer') as mock:
        mock_instance = mock.return_value
        mock_instance.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        mock_instance.get_sentence_embedding_dimension.return_value = 3
        yield mock

@pytest.fixture
def mock_faiss():
    """Fixture to mock the FAISS index."""
    with patch('memory.faiss') as mock:
        mock_index = MagicMock()
        mock_index.ntotal = 0
        mock_index.add.return_value = None
        mock_index.search.return_value = (np.array([[1.0]]), np.array([[0]]))
        mock.read_index.return_value = mock_index
        mock.IndexFlatL2.return_value = mock_index
        yield mock

def test_initialization_new(mock_sentence_transformer, mock_faiss):
    """Tests that the MemoryStore initializes correctly when no files exist."""
    with patch('os.path.exists', return_value=False):
        memory_store = MemoryStore()
        assert memory_store.dimension == 3
        mock_faiss.IndexFlatL2.assert_called_once_with(3)
        assert memory_store.store == {}

def test_initialization_existing(mock_sentence_transformer, mock_faiss):
    """Tests that the MemoryStore initializes correctly when files exist."""
    with patch('os.path.exists', return_value=True):
        m = mock_open(read_data='{"0": "test"}')
        with patch('builtins.open', m):
            memory_store = MemoryStore()
            assert memory_store.dimension == 3
            mock_faiss.read_index.assert_called_once()
            assert memory_store.store == {"0": "test"}

def test_add(mock_sentence_transformer, mock_faiss):
    """Tests the add method."""
    with patch('os.path.exists', return_value=False):
        memory_store = MemoryStore()
        with patch.object(memory_store, '_save') as mock_save:
            memory_store.add("test text")
            mock_sentence_transformer.return_value.encode.assert_called_once_with(["test text"])
            mock_faiss.IndexFlatL2.return_value.add.assert_called_once()
            assert memory_store.store == {"0": "test text"}
            mock_save.assert_called_once()

def test_search(mock_sentence_transformer, mock_faiss):
    """Tests the search method."""
    with patch('os.path.exists', return_value=True):
        m = mock_open(read_data='{"0": "test"}')
        with patch('builtins.open', m):
            memory_store = MemoryStore()
            memory_store.index.ntotal = 1
            results = memory_store.search("test query")
            mock_sentence_transformer.return_value.encode.assert_called_once_with(["test query"])
            mock_faiss.read_index.return_value.search.assert_called_once()
            assert results == ["test"]

def test_search_empty(mock_sentence_transformer, mock_faiss):
    """Tests the search method with an empty index."""
    with patch('os.path.exists', return_value=False):
        memory_store = MemoryStore()
        results = memory_store.search("test query")
        assert results == []

def test_save(mock_sentence_transformer, mock_faiss):
    """Tests the _save method."""
    with patch('os.path.exists', return_value=False):
        m = mock_open()
        with patch('builtins.open', m):
            memory_store = MemoryStore()
            memory_store.store = {"0": "test"}
            memory_store._save()
            mock_faiss.write_index.assert_called_once_with(memory_store.index, memory_store.index_file)
            m.assert_called_once_with(memory_store.store_file, 'w')
            handle = m()
            expected_json = json.dumps({"0": "test"})
            # Check that the mock was called with the JSON string
            # We can't use assert_called_once_with because json.dump writes in chunks
            assert any(call(expected_json) for call in handle.write.call_args_list)

@pytest.fixture
def memory_store_with_sqlite(mock_sentence_transformer, mock_faiss):
    with patch('os.path.exists', return_value=False):
        memory_store = MemoryStore(sqlite_file=":memory:")
        yield memory_store

def test_sqlite_initialization(memory_store_with_sqlite):
    """Tests that SQLite tables are created."""
    cursor = memory_store_with_sqlite.conn.cursor()

    # Check memories table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='memories'")
    assert cursor.fetchone() is not None

    # Check consolidations table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='consolidations'")
    assert cursor.fetchone() is not None

def test_add_and_get_memory(memory_store_with_sqlite):
    """Tests adding and retrieving a memory."""
    memory_id = memory_store_with_sqlite.add_memory(
        source="user_input",
        raw_text="The quick brown fox jumps over the lazy dog.",
        summary="Fox jumps dog",
        entities=["fox", "dog"],
        topics=["animals"],
        importance=5
    )
    assert memory_id == 1

    memory = memory_store_with_sqlite.get_memory(memory_id)
    assert memory is not None
    assert memory['source'] == "user_input"
    assert memory['raw_text'] == "The quick brown fox jumps over the lazy dog."
    assert memory['summary'] == "Fox jumps dog"
    assert memory['entities'] == ["fox", "dog"]
    assert memory['topics'] == ["animals"]
    assert memory['importance'] == 5
    assert memory['consolidated'] is False

def test_add_and_get_consolidation(memory_store_with_sqlite):
    """Tests adding and retrieving a consolidation."""
    consolidation_id = memory_store_with_sqlite.add_consolidation(
        source_ids=[1, 2, 3],
        summary="A summary of multiple memories",
        insight="A new insight derived from them"
    )
    assert consolidation_id == 1

    consolidation = memory_store_with_sqlite.get_consolidation(consolidation_id)
    assert consolidation is not None
    assert consolidation['source_ids'] == [1, 2, 3]
    assert consolidation['summary'] == "A summary of multiple memories"
    assert consolidation['insight'] == "A new insight derived from them"

def test_get_unconsolidated_memories(memory_store_with_sqlite):
    """Tests fetching unconsolidated memories."""
    # Add one unconsolidated
    memory_store_with_sqlite.add_memory(source="test", raw_text="text1")
    # Add one consolidated
    memory_store_with_sqlite.add_memory(source="test", raw_text="text2", consolidated=True)

    unconsolidated = memory_store_with_sqlite.get_unconsolidated_memories()
    assert len(unconsolidated) == 1
    assert unconsolidated[0]['raw_text'] == "text1"

def test_mark_memory_consolidated(memory_store_with_sqlite):
    """Tests marking a memory as consolidated."""
    memory_id = memory_store_with_sqlite.add_memory(source="test", raw_text="text1")

    # Verify unconsolidated
    memory = memory_store_with_sqlite.get_memory(memory_id)
    assert memory['consolidated'] is False

    # Mark consolidated
    memory_store_with_sqlite.mark_memory_consolidated(memory_id)

    # Verify consolidated
    memory = memory_store_with_sqlite.get_memory(memory_id)
    assert memory['consolidated'] is True

@patch('os.getenv')
def test_encryption_decryption(mock_getenv, mock_sentence_transformer, mock_faiss):
    """Tests that SQLite data is encrypted and decrypted properly."""
    from cryptography.fernet import Fernet
    mock_getenv.return_value = Fernet.generate_key().decode()

    with patch('os.path.exists', return_value=False):
        memory_store = MemoryStore(sqlite_file=":memory:")

    memory_id = memory_store.add_memory(
        source="secret_source",
        raw_text="This is a secret",
        summary="Secret summary",
        entities=["secret_entity"]
    )

    # Verify raw database contains encrypted data
    cursor = memory_store.conn.cursor()
    cursor.execute("SELECT raw_text, summary, entities FROM memories WHERE id = ?", (memory_id,))
    row = cursor.fetchone()

    assert row['raw_text'] != "This is a secret"
    assert row['raw_text'].startswith("gAAAAA")
    assert row['summary'] != "Secret summary"
    assert row['entities'] != '["secret_entity"]'

    # Verify retrieved memory is decrypted
    memory = memory_store.get_memory(memory_id)
    assert memory['raw_text'] == "This is a secret"
    assert memory['summary'] == "Secret summary"
    assert memory['entities'] == ["secret_entity"]
