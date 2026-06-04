import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the path to the pipecatapp directory to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp/tools')))

from rag_tool import load_document_cached
import rag_tool

def test_strict_caching():
    # We want to patch TextLoader in rag_tool namespace so it returns our mock
    mock_loader_instance = MagicMock()
    mock_loader_instance.load.return_value = ["mock_doc"]

    mock_loader_class = MagicMock(return_value=mock_loader_instance)

    # We also need to patch os.path.getmtime
    with patch('rag_tool.os.path.getmtime', return_value=12345.0) as mock_mtime:
        # We need to monkeypatch the internal TextLoader import since it's imported inside the function
        import langchain_community.document_loaders
        with patch('langchain_community.document_loaders.TextLoader', new=mock_loader_class):

            # Clear the LRU cache before starting
            rag_tool._load_document_cached_internal.cache_clear()

            # First call
            doc1 = load_document_cached('dummy.txt')
            assert doc1 == ["mock_doc"]
            mock_loader_class.assert_called_once_with('dummy.txt', encoding='utf-8')

            # Second call, mtime unchanged
            doc2 = load_document_cached('dummy.txt')
            assert doc2 == ["mock_doc"]
            assert mock_loader_class.call_count == 1 # Should not be called again

            # Third call, mtime changed
            mock_mtime.return_value = 54321.0
            doc3 = load_document_cached('dummy.txt')
            assert doc3 == ["mock_doc"]
            assert mock_loader_class.call_count == 2 # Called again because mtime changed
