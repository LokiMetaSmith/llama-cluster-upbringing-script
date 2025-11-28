import pytest
import os
import sys
from unittest.mock import MagicMock, patch, mock_open
import threading

# Add the path to the RAG tool
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

import numpy as np # Now safe to import
from rag_tool import RAG_Tool

@pytest.fixture
def mock_sentence_transformer():
    """Fixture to mock the SentenceTransformer."""
    with patch('rag_tool.SentenceTransformer') as mock:
        # Mock the encode method to return a dummy embedding
        mock_instance = mock.return_value
        # Use mock numpy array
        mock_instance.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        yield mock

@pytest.fixture
def mock_faiss():
    """Fixture to mock the FAISS index."""
    with patch('rag_tool.faiss') as mock:
        # Mock the IndexFlatL2 and its methods
        mock_index = MagicMock()
        mock_index.add.return_value = None
        # Return 3 results to match k=3 in the search function
        mock_index.search.return_value = (np.array([[1.0, 2.0, 3.0]]), np.array([[0, 1, 2]]))
        mock.IndexFlatL2.return_value = mock_index
        yield mock

@pytest.fixture
def mock_pmm_memory():
    """Fixture to mock the PMMMemory object."""
    mock_memory = MagicMock()
    mock_memory.get_events.return_value = []
    mock_memory.add_event.return_value = None
    return mock_memory

@pytest.fixture(autouse=True)
def sync_threading(monkeypatch):
    """Forces threading.Thread to run synchronously for predictable tests."""
    class SyncThread:
        def __init__(self, target, daemon=False):
            self.target = target
        def start(self):
            self.target()
    monkeypatch.setattr(threading, 'Thread', SyncThread)

def test_rag_tool_initialization(mock_sentence_transformer, mock_faiss, mock_pmm_memory):
    """Tests that the RAG_Tool initializes without errors and builds from filesystem if memory is empty."""
    with patch('os.walk') as mock_walk:
        mock_walk.return_value = [
            ('/fake/dir', [], ['test.md'])
        ]
        m = mock_open(read_data="This is a test file.")
        with patch('builtins.open', m):
            # Simulate memory being empty, then populated after scan
            mock_pmm_memory.get_events.side_effect = [
                [],
                [{'content': 'This is a test file.', 'meta': {'source': '/fake/dir/test.md'}}]
            ]

            tool = RAG_Tool(pmm_memory=mock_pmm_memory, base_dir="/fake/dir")

            assert tool.is_ready
            mock_pmm_memory.add_event.assert_called_once_with(
                kind="rag_document",
                content="This is a test file.",
                meta={"source": "/fake/dir/test.md"}
            )
            mock_faiss.IndexFlatL2.return_value.add.assert_called_once()

def test_rag_tool_search(mock_sentence_transformer, mock_faiss, mock_pmm_memory):
    """Tests the search functionality of the RAG_Tool."""
    # Simulate that documents already exist in memory
    docs = [
        {'content': "This is chunk 1.", 'meta': {"source": "/fake/dir/test1.md"}},
        {'content': "This is chunk 2.", 'meta': {"source": "/fake/dir/test2.txt"}},
        {'content': "This is chunk 3.", 'meta': {"source": "/fake/dir/test3.md"}}
    ]
    mock_pmm_memory.get_events.return_value = docs

    with patch('os.walk') as mock_walk: # os.walk should not be called now
        tool = RAG_Tool(pmm_memory=mock_pmm_memory, base_dir="/fake/dir")
        assert tool.is_ready
        mock_walk.assert_not_called()

        # Perform a search
        results = tool.search_knowledge_base("test query")

        # Verify that the search method was called on the index
        mock_faiss.IndexFlatL2.return_value.search.assert_called_once()
        assert "From /fake/dir/test1.md" in results
        assert "This is chunk 1." in results
        assert "From /fake/dir/test2.txt" in results
        assert "This is chunk 2." in results
        assert "From /fake/dir/test3.md" in results
        assert "This is chunk 3." in results

def test_rag_tool_empty_knowledge_base(mock_sentence_transformer, mock_faiss, mock_pmm_memory):
    """Tests that the RAG tool handles an empty knowledge base gracefully."""
    # Memory is empty
    mock_pmm_memory.get_events.return_value = []

    with patch('os.walk') as mock_walk:
        # Filesystem is empty
        mock_walk.return_value = []

        tool = RAG_Tool(pmm_memory=mock_pmm_memory, base_dir="/fake/dir")

        assert tool.is_ready
        assert tool.index is None
        assert tool.documents == []
        result = tool.search_knowledge_base("any query")
        assert result == "The knowledge base is empty. I cannot answer questions about the project yet."

def test_no_relevant_documents_found(mock_sentence_transformer, mock_faiss, mock_pmm_memory):
    """Tests the case where the search returns no relevant documents."""
    # Simulate that documents already exist in memory
    docs = [{'content': "This is a test file.", 'meta': {"source": "/fake/dir/test.md"}}]
    mock_pmm_memory.get_events.return_value = docs

    tool = RAG_Tool(pmm_memory=mock_pmm_memory, base_dir="/fake/dir")
    assert tool.is_ready

    # Mock the FAISS search to return no results
    mock_faiss.IndexFlatL2.return_value.search.return_value = (np.array([[-1, -1, -1]]), np.array([[-1, -1, -1]]))

    # Perform a search
    results = tool.search_knowledge_base("test query")
    assert results == "I could not find any relevant information in the knowledge base to answer your question."

def test_rag_tool_search_with_fewer_than_k_results(mock_sentence_transformer, mock_faiss, mock_pmm_memory):
    """Tests that search works correctly when the knowledge base has fewer than k documents."""
    # Simulate that documents already exist in memory
    docs = [
        {'content': "This is chunk 1.", 'meta': {"source": "/fake/dir/test1.md"}},
        {'content': "This is chunk 2.", 'meta': {"source": "/fake/dir/test2.txt"}}
    ]
    mock_pmm_memory.get_events.return_value = docs

    tool = RAG_Tool(pmm_memory=mock_pmm_memory, base_dir="/fake/dir")
    assert tool.is_ready

    # Mock the FAISS search to return only 2 valid results
    mock_faiss.IndexFlatL2.return_value.search.return_value = (np.array([[1.0, 2.0, -1.0]]), np.array([[0, 1, -1]]))

    # Perform a search
    results = tool.search_knowledge_base("test query")

    # Verify that the search method was called on the index
    mock_faiss.IndexFlatL2.return_value.search.assert_called_once()
    assert "From /fake/dir/test1.md" in results
    assert "This is chunk 1." in results
    assert "From /fake/dir/test2.txt" in results
    assert "This is chunk 2." in results
