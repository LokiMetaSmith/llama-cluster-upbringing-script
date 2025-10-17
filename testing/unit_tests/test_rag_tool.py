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
        mock_index.search.return_value = (np.array([[1.0, 1.0, 1.0]]), np.array([[0, 0, 0]]))
        mock.IndexFlatL2.return_value = mock_index
        yield mock

@pytest.fixture
def mock_text_splitter():
    """Fixture to mock the RecursiveCharacterTextSplitter."""
    with patch('tools.rag_tool.RecursiveCharacterTextSplitter') as mock:
        mock_instance = mock.return_value
        # Mock create_documents to return a list of mock documents
        mock_doc = MagicMock()
        mock_doc.page_content = "This is a test chunk."
        mock_instance.create_documents.return_value = [mock_doc]
        yield mock

def test_rag_tool_initialization(mock_sentence_transformer, mock_faiss, mock_text_splitter):
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


def test_rag_tool_search(mock_sentence_transformer, mock_faiss, mock_text_splitter):
    """Tests the search functionality of the RAG_Tool."""
    with patch('os.walk') as mock_walk:
        mock_walk.return_value = [('/fake/dir', [], ['test.md'])]
        m = mock_open(read_data="This is a test file.")
        with patch('builtins.open', m):
            tool = RAG_Tool(base_dir="/fake/dir")
            # Mock the document list after it has been populated
            mock_doc = MagicMock()
            mock_doc.page_content = "This is a test chunk."
            mock_doc.metadata = {"source": "/fake/dir/test.md"}
            tool.documents = [mock_doc]

            # Perform a search
            results = tool.search_knowledge_base("test query")

            # Verify that the search method was called on the index
            mock_faiss.IndexFlatL2.return_value.search.assert_called_once()
            assert "From /fake/dir/test.md" in results
            assert "This is a test chunk." in results

def test_rag_tool_empty_knowledge_base(mock_sentence_transformer, mock_faiss, mock_text_splitter):
    """Tests that the RAG tool handles an empty knowledge base gracefully."""
    with patch('os.walk') as mock_walk:
        # Simulate no files being found
        mock_walk.return_value = []
        tool = RAG_Tool(base_dir="/fake/dir")
        assert tool.index is None
        assert tool.documents == []
        result = tool.search_knowledge_base("any query")
        assert result == "The knowledge base is empty. I cannot answer questions about the project yet."