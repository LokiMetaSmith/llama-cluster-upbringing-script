import pytest
import os
import sys
import numpy as np
from unittest.mock import MagicMock, patch, mock_open

# Add the path to the RAG tool
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files')))

from tools.rag_tool import RAG_Tool

@pytest.fixture
def mock_sentence_transformer():
    """Fixture to mock the SentenceTransformer."""
    with patch('tools.rag_tool.SentenceTransformer') as mock:
        # Mock the encode method to return a dummy embedding
        mock_instance = mock.return_value
        mock_instance.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        yield mock

@pytest.fixture
def mock_faiss():
    """Fixture to mock the FAISS index."""
    with patch('tools.rag_tool.faiss') as mock:
        # Mock the IndexFlatL2 and its methods
        mock_index = MagicMock()
        mock_index.add.return_value = None
        # Return 3 results to match k=3 in the search function
        mock_index.search.return_value = (np.array([[1.0, 2.0, 3.0]]), np.array([[0, 1, 2]]))
        mock.IndexFlatL2.return_value = mock_index
        yield mock

def test_rag_tool_initialization(mock_sentence_transformer, mock_faiss):
    """Tests that the RAG_Tool initializes without errors."""
    # Mock os.walk to return a controlled set of files
    with patch('os.walk') as mock_walk:
        mock_walk.return_value = [
            ('/fake/dir', ['subdir'], ['test.md']),
            ('/fake/dir/subdir', [], ['another.txt'])
        ]
        # Mock open to simulate reading file content
        m = mock_open(read_data="This is a test file.")
        with patch('builtins.open', m):
            tool = RAG_Tool(base_dir="/fake/dir")
            assert tool is not None
            assert tool.index is not None
            # Verify that encode was called
            mock_sentence_transformer.return_value.encode.assert_called()
            # Verify that the index was created and populated
            mock_faiss.IndexFlatL2.assert_called_once()
            mock_faiss.IndexFlatL2.return_value.add.assert_called_once()


def test_rag_tool_search(mock_sentence_transformer, mock_faiss):
    """Tests the search functionality of the RAG_Tool."""
    with patch('os.walk') as mock_walk:
        mock_walk.return_value = [('/fake/dir', [], ['test.md'])]
        m = mock_open(read_data="This is a test file.")
        with patch('builtins.open', m):
            tool = RAG_Tool(base_dir="/fake/dir")
            # Mock the document list after it has been populated
            doc1 = type('obj', (object,), {'page_content': "This is chunk 1.", 'metadata': {"source": "/fake/dir/test1.md"}})
            doc2 = type('obj', (object,), {'page_content': "This is chunk 2.", 'metadata': {"source": "/fake/dir/test2.txt"}})
            doc3 = type('obj', (object,), {'page_content': "This is chunk 3.", 'metadata': {"source": "/fake/dir/test3.md"}})
            tool.documents = [doc1, doc2, doc3]

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

def test_rag_tool_empty_knowledge_base(mock_sentence_transformer, mock_faiss):
    """Tests that the RAG tool handles an empty knowledge base gracefully."""
    with patch('os.walk') as mock_walk:
        # Simulate no files being found
        mock_walk.return_value = []
        tool = RAG_Tool(base_dir="/fake/dir")
        assert tool.index is None
        assert tool.documents == []
        result = tool.search_knowledge_base("any query")
        assert result == "The knowledge base is empty. I cannot answer questions about the project yet."

def test_no_relevant_documents_found(mock_sentence_transformer, mock_faiss):
    """Tests the case where the search returns no relevant documents."""
    with patch('os.walk') as mock_walk:
        mock_walk.return_value = [('/fake/dir', [], ['test.md'])]
        m = mock_open(read_data="This is a test file.")
        with patch('builtins.open', m):
            tool = RAG_Tool(base_dir="/fake/dir")
            # Mock the FAISS search to return no results
            mock_faiss.IndexFlatL2.return_value.search.return_value = (np.array([[-1, -1, -1]]), np.array([[-1, -1, -1]]))
            # Perform a search
            results = tool.search_knowledge_base("test query")
            assert results == "I could not find any relevant information in the knowledge base to answer your question."

def test_rag_tool_search_with_fewer_than_k_results(mock_sentence_transformer, mock_faiss):
    """Tests that search works correctly when the knowledge base has fewer than k documents."""
    with patch('os.walk') as mock_walk:
        mock_walk.return_value = [('/fake/dir', [], ['test.md'])]
        m = mock_open(read_data="This is a test file.")
        with patch('builtins.open', m):
            tool = RAG_Tool(base_dir="/fake/dir")
            # Mock the document list with only 2 documents
            doc1 = type('obj', (object,), {'page_content': "This is chunk 1.", 'metadata': {"source": "/fake/dir/test1.md"}})
            doc2 = type('obj', (object,), {'page_content': "This is chunk 2.", 'metadata': {"source": "/fake/dir/test2.txt"}})
            tool.documents = [doc1, doc2]

            # Mock the FAISS search to return only 2 results, as if k=3 but only 2 docs exist
            mock_faiss.IndexFlatL2.return_value.search.return_value = (np.array([[1.0, 2.0]]), np.array([[0, 1]]))

            # Perform a search
            results = tool.search_knowledge_base("test query")

            # Verify that the search method was called on the index
            mock_faiss.IndexFlatL2.return_value.search.assert_called_once()
            assert "From /fake/dir/test1.md" in results
            assert "This is chunk 1." in results
            assert "From /fake/dir/test2.txt" in results
            assert "This is chunk 2." in results