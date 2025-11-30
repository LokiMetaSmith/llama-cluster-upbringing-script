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
