import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os
import numpy as np

# Define modules to mock before importing anything
mock_modules = {
    "extism": MagicMock(),
    "pmm_memory": MagicMock(),
    "ultralytics": MagicMock(),
    "sentence_transformers": MagicMock(),
    "faiss": MagicMock(),
    "chromadb": MagicMock(),
    "chromadb.config": MagicMock(),
    "langchain_community": MagicMock(),
    "langchain_community.document_loaders": MagicMock(),
    "langchain_text_splitters": MagicMock()
}

# Torch mock needs to have __spec__ to satisfy transformers
mock_torch = MagicMock()
mock_torch.__spec__ = MagicMock()
mock_modules["torch"] = mock_torch

@pytest.fixture(scope="module", autouse=True)
def setup_mocks():
    with patch.dict(sys.modules, mock_modules):
        yield

@pytest.fixture
def mock_llm_client():
    client = MagicMock()
    client.process_text = AsyncMock()
    return client

@pytest.fixture
def pruner(mock_llm_client):
    from pipecatapp.utils.rag_pruner import RAGPruner
    return RAGPruner(llm_client=mock_llm_client)

@pytest.mark.asyncio
async def test_rag_pruner_grading(pruner, mock_llm_client):
    query = "How do I use API X?"
    chunks = [
        {"id": "chunk1", "content": "To use API X, do this..."},
        {"id": "chunk2", "content": "API Y is unrelated."}
    ]

    # Mock LLM response
    mock_llm_client.process_text.return_value = json.dumps({"chunk1": 5, "chunk2": 1})

    grades = await pruner.prune_chunks(query, chunks)

    assert grades["chunk1"] == 5
    assert grades["chunk2"] == 1
    assert mock_llm_client.process_text.called

@pytest.mark.asyncio
async def test_rag_pruner_json_extraction(pruner, mock_llm_client):
    # Test that it can extract JSON from markdown-like chatter
    mock_llm_client.process_text.return_value = "Here is the grading: ```json\n{\"c1\": 4}\n```"
    chunks = [{"id": "c1", "content": "some content"}]

    grades = await pruner.prune_chunks("query", chunks)
    assert grades["c1"] == 4

@pytest.mark.asyncio
async def test_rag_tool_with_pruning():
    from pipecatapp.tools.rag_tool import RAG_Tool

    mock_memory = MagicMock()
    mock_pruner = MagicMock()
    mock_pruner.prune_chunks = AsyncMock()

    with patch("pipecatapp.tools.rag_tool.SentenceTransformer") as mock_st_class:
        mock_model = mock_st_class.return_value
        mock_model.get_sentence_embedding_dimension.return_value = 384
        # Return a numpy array to support .tolist()
        mock_model.encode.return_value = np.array([[0.1] * 384], dtype=np.float32)

        tool = RAG_Tool(
            pmm_memory=mock_memory,
            base_dir="/tmp",
            pruner=mock_pruner,
            pruning_threshold=4,
            keep_top_k=1
        )
        tool.is_ready = True
        tool.initialization_error = None

        # Mock ChromaDB result
        mock_collection = tool.chroma_client.get_collection.return_value
        mock_collection.query.return_value = {
            "documents": [["doc1", "doc2", "doc3"]],
            "metadatas": [[{"source": "src1"}, {"source": "src2"}, {"source": "src3"}]],
            "ids": [["id1", "id2", "id3"]]
        }

        # Mock pruner grades: id1 is top-k (kept anyway), id2 is high (kept), id3 is low (pruned)
        mock_pruner.prune_chunks.return_value = {"id1": "1", "id2": "5", "id3": "2"}

        results_str = await tool.search_knowledge_base("my query", k=3)

        assert "src1" in results_str # Kept because i < keep_top_k (0 < 1)
        assert "src2" in results_str # Kept because grade (5) >= threshold (4)
        assert "src3" not in results_str # Pruned because grade (2) < threshold (4) and i >= keep_top_k
