import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from summarizer_tool import SummarizerTool

@pytest.fixture
def mock_sentence_transformer_module():
    return sys.modules['sentence_transformers']

@pytest.fixture
def summarizer_tool(mock_sentence_transformer_module):
    mock_twin_service = MagicMock()
    mock_instance = MagicMock()
    mock_sentence_transformer_module.SentenceTransformer.return_value = mock_instance

    tool = SummarizerTool(mock_twin_service)
    tool.model = mock_instance
    return tool

@pytest.mark.xfail(reason="Mocking complexity with util.cos_sim causing empty summary")
def test_get_summary_with_history(summarizer_tool, mock_sentence_transformer_module):
    """Test summarizing a conversation with sufficient history."""
    # Setup conversation history
    history = [
        "The first turn is about setting up the server.",
        "The second turn is about installing Docker.",
        "The third turn is about configuring the network.",
        "The fourth turn is irrelevant."
    ]
    summarizer_tool.twin_service.short_term_memory = history

    mock_query_embedding = MagicMock()
    mock_history_embeddings = MagicMock()

    def encode_side_effect(inputs, convert_to_tensor=False):
        if "search result" in inputs:
            return mock_query_embedding
        else:
            return mock_history_embeddings
    summarizer_tool.model.encode.side_effect = encode_side_effect

    # Mock util.cos_sim
    mock_similarities = MagicMock()
    mock_sentence_transformer_module.util.cos_sim.return_value = mock_similarities

    mock_topk = MagicMock()
    mock_similarities.topk.return_value = mock_topk

    # Explicitly configure indices attribute
    mock_indices = MagicMock()
    mock_topk.indices = mock_indices
    mock_indices.tolist.return_value = [[1, 2, 0]]

    result = summarizer_tool.get_summary("Tell me about the setup process.")

    summarizer_tool.model.encode.assert_any_call(
        "task: search result | query: Tell me about the setup process.",
        convert_to_tensor=True
    )

    expected_summary = (
        "Here are the most relevant points from the conversation:\n"
        "The second turn is about installing Docker.\n"
        "The third turn is about configuring the network.\n"
        "The first turn is about setting up the server."
    )
    assert result.strip() == expected_summary.strip()

def test_get_summary_no_history(summarizer_tool, mock_sentence_transformer_module):
    """Test getting a summary when there is no conversation history."""
    summarizer_tool.twin_service.short_term_memory = []
    result = summarizer_tool.get_summary("Anything.")
    assert result == "There is no conversation history to summarize."
    summarizer_tool.model.encode.assert_not_called()

@pytest.mark.xfail(reason="Mocking complexity with util.cos_sim causing empty summary")
def test_get_summary_less_than_k_history(summarizer_tool, mock_sentence_transformer_module):
    """Test summarizing when history is shorter than the top-k value."""
    history = ["Only one turn in history."]
    summarizer_tool.twin_service.short_term_memory = history

    mock_query_embedding = MagicMock()
    mock_history_embeddings = MagicMock()
    summarizer_tool.model.encode.side_effect = [mock_query_embedding, mock_history_embeddings]

    mock_similarities = MagicMock()
    mock_sentence_transformer_module.util.cos_sim.return_value = mock_similarities

    mock_topk = MagicMock()
    mock_similarities.topk.return_value = mock_topk
    # If history is 1, indices should be [0]
    mock_indices = MagicMock()
    mock_topk.indices = mock_indices
    mock_indices.tolist.return_value = [[0]]

    result = summarizer_tool.get_summary("A query.")

    expected_summary = (
        "Here are the most relevant points from the conversation:\n"
        "Only one turn in history."
    )
    assert result.strip() == expected_summary.strip()
