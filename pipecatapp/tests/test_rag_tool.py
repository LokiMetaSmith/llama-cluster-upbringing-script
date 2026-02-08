import pytest
import os
import sys
from unittest.mock import MagicMock, patch

# Setup mocks for dependencies
mock_faiss = MagicMock()
mock_st = MagicMock()
mock_st.SentenceTransformer = MagicMock()
mock_numpy = MagicMock()

modules_to_patch = {
    "faiss": mock_faiss,
    "sentence_transformers": mock_st,
    "numpy": mock_numpy
}

@pytest.fixture
def rag_tool_class():
    with patch.dict(sys.modules, modules_to_patch):
        # We need to make sure pmm_memory is importable or mocked
        # If running from root, pipecatapp needs to be in path
        if "pipecatapp" not in sys.modules:
             sys.path.append(os.getcwd())

        from pipecatapp.tools.rag_tool import RAG_Tool
        yield RAG_Tool

@pytest.fixture
def mock_memory():
    class MockPMMMemory:
        def __init__(self):
            self.events = []
        def get_events_sync(self, kind=None, limit=10):
            return self.events
        def add_event_sync(self, kind, content, meta=None):
            self.events.append({"kind": kind, "content": content, "meta": meta or {}})
    return MockPMMMemory()

@pytest.fixture
def test_dirs(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    (root / "doc1.txt").write_text("content 1")
    subdir = root / "subdir"
    subdir.mkdir()
    (subdir / "doc2.txt").write_text("content 2")
    forbidden = tmp_path / "forbidden"
    forbidden.mkdir()
    return root, subdir, forbidden

def test_rag_scope_security(rag_tool_class, mock_memory, test_dirs):
    root, subdir, forbidden = test_dirs

    # Setup mock return for encode
    mock_model_instance = mock_st.SentenceTransformer.return_value
    mock_array = MagicMock()
    mock_array.shape = (1, 384)
    mock_model_instance.encode.return_value = mock_array

    tool = rag_tool_class(pmm_memory=mock_memory, base_dir=str(root), allowed_root=str(root))

    assert tool.base_dir == str(root)
    assert tool.set_scope(str(subdir)) is True
    assert tool.base_dir == str(subdir)
    assert tool.set_scope(str(forbidden)) is False
    assert tool.base_dir == str(subdir)
    assert tool.set_scope(str(root)) is True

def test_rag_filtering(rag_tool_class, mock_memory, test_dirs):
    root, subdir, forbidden = test_dirs

    mock_model_instance = mock_st.SentenceTransformer.return_value
    mock_array = MagicMock()
    mock_array.shape = (1, 384)
    mock_model_instance.encode.return_value = mock_array

    mock_memory.add_event_sync("rag_document", "doc1", {"source": str(root / "doc1.txt")})
    mock_memory.add_event_sync("rag_document", "doc2", {"source": str(subdir / "doc2.txt")})
    mock_memory.add_event_sync("rag_document", "external", {"source": "/external/path"})

    tool = rag_tool_class(pmm_memory=mock_memory, base_dir=str(root), allowed_root=str(root))
    tool._build_knowledge_base()

    sources = [d['meta']['source'] for d in tool.documents]
    assert str(root / "doc1.txt") in sources
    assert str(subdir / "doc2.txt") in sources
    assert "/external/path" not in sources

    tool.set_scope(str(subdir))
    tool._build_knowledge_base()

    sources = [d['meta']['source'] for d in tool.documents]
    assert str(root / "doc1.txt") not in sources
    assert str(subdir / "doc2.txt") in sources

def test_rag_sibling_directory_isolation(rag_tool_class, mock_memory, test_dirs):
    root, subdir, forbidden = test_dirs

    # Create a sibling directory that shares prefix with 'subdir'
    sibling = root / "subdir-secret"
    sibling.mkdir()
    (sibling / "secret.txt").write_text("secret content")

    mock_model_instance = mock_st.SentenceTransformer.return_value
    mock_array = MagicMock()
    mock_array.shape = (1, 384)
    mock_model_instance.encode.return_value = mock_array

    mock_memory.add_event_sync("rag_document", "doc_in_subdir", {"source": str(subdir / "doc2.txt")})
    mock_memory.add_event_sync("rag_document", "doc_in_sibling", {"source": str(sibling / "secret.txt")})

    # Tool initialized with scope 'subdir'
    tool = rag_tool_class(pmm_memory=mock_memory, base_dir=str(subdir), allowed_root=str(root))
    tool._build_knowledge_base()

    sources = [d['meta']['source'] for d in tool.documents]
    assert str(subdir / "doc2.txt") in sources
    assert str(sibling / "secret.txt") not in sources

def test_rag_mandatory_base_dir(rag_tool_class, mock_memory):
    """Test that RAG_Tool raises ValueError if base_dir is missing."""
    with pytest.raises(ValueError, match="base_dir must be provided"):
        rag_tool_class(pmm_memory=mock_memory)

def test_rag_root_scan_protection(rag_tool_class, mock_memory):
    """Test that RAG_Tool blocks scanning root (/) by default."""
    # Should fail without allow_root_scan=True
    with pytest.raises(ValueError, match="Scanning the filesystem root"):
        rag_tool_class(pmm_memory=mock_memory, base_dir="/")

    # Should pass with allow_root_scan=True
    tool = rag_tool_class(pmm_memory=mock_memory, base_dir="/", allow_root_scan=True)
    assert tool.base_dir == "/"
