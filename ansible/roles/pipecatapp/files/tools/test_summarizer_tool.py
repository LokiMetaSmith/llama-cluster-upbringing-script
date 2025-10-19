import unittest
from unittest.mock import patch, MagicMock
import torch

# Due to the way the class is structured, we need to patch the SentenceTransformer
# before it's imported by the tool.
with patch('sentence_transformers.SentenceTransformer') as mock_sentence_transformer:
    # We can configure the mock instance that will be created inside the tool
    mock_model_instance = MagicMock()
    mock_sentence_transformer.return_value = mock_model_instance
    from summarizer_tool import SummarizerTool

class TestSummarizerTool(unittest.TestCase):

    def setUp(self):
        """Set up mock objects before each test."""
        self.mock_twin_service = MagicMock()

        # We need to re-assign the mock for every test instance
        self.mock_model = mock_model_instance
        self.mock_model.reset_mock() # Reset mock state between tests

        # Now, instantiate the tool. It will get the mocked model.
        self.summarizer_tool = SummarizerTool(self.mock_twin_service)

    def test_get_summary_with_history(self):
        """Test summarizing a conversation with sufficient history."""
        # Setup conversation history
        history = [
            "The first turn is about setting up the server.",
            "The second turn is about installing Docker.",
            "The third turn is about configuring the network.",
            "The fourth turn is irrelevant."
        ]
        self.mock_twin_service.short_term_memory = history

        # Mock the sentence embedding model's behavior
        # Let's pretend the query is most similar to the 2nd, 3rd, and 1st turns in that order.
        mock_query_embedding = torch.tensor([[1.0, 0.0]])
        mock_history_embeddings = torch.tensor([
            [0.8, 0.2],  # 1st
            [0.9, 0.1],  # 2nd
            [0.85, 0.15], # 3rd
            [0.1, 0.9]   # 4th
        ])

        # Mock the model's encode method
        def encode_side_effect(inputs, convert_to_tensor):
            if "search result" in inputs: # This is the query
                return mock_query_embedding
            else: # This is the history
                return mock_history_embeddings
        self.mock_model.encode.side_effect = encode_side_effect

        # Mock the similarity calculation to return predictable results
        # The similarity scores correspond to the history embeddings above.
        mock_similarities = torch.tensor([[0.98, 0.99, 0.985, 0.2]])

        # We need to patch 'util.cos_sim' within the summarizer_tool's module scope
        with patch('summarizer_tool.util.cos_sim', return_value=mock_similarities):
            result = self.summarizer_tool.get_summary("Tell me about the setup process.")

            # Verify the correct prefixes were used for encoding
            self.mock_model.encode.assert_any_call(
                "task: search result | query: Tell me about the setup process.",
                convert_to_tensor=True
            )
            expected_history_call = [
                "title: none | text: The first turn is about setting up the server.",
                "title: none | text: The second turn is about installing Docker.",
                "title: none | text: The third turn is about configuring the network.",
                "title: none | text: The fourth turn is irrelevant."
            ]
            self.mock_model.encode.assert_any_call(
                expected_history_call,
                convert_to_tensor=True
            )

            # The topk(3) indices of our mock similarities are 1, 2, 0
            expected_summary = (
                "Here are the most relevant points from the conversation:\n"
                "The second turn is about installing Docker.\n"
                "The third turn is about configuring the network.\n"
                "The first turn is about setting up the server."
            )
            self.assertEqual(result.strip(), expected_summary.strip())

    def test_get_summary_no_history(self):
        """Test getting a summary when there is no conversation history."""
        self.mock_twin_service.short_term_memory = []
        result = self.summarizer_tool.get_summary("Anything.")
        self.assertEqual(result, "There is no conversation history to summarize.")
        self.mock_model.encode.assert_not_called()

    def test_get_summary_less_than_k_history(self):
        """Test summarizing when history is shorter than the top-k value."""
        history = ["Only one turn in history."]
        self.mock_twin_service.short_term_memory = history

        mock_query_embedding = torch.tensor([[1.0, 0.0]])
        mock_history_embeddings = torch.tensor([[0.9, 0.1]])
        self.mock_model.encode.side_effect = [mock_query_embedding, mock_history_embeddings]

        with patch('summarizer_tool.util.cos_sim', return_value=torch.tensor([[0.99]])):
            result = self.summarizer_tool.get_summary("A query.")

            expected_summary = (
                "Here are the most relevant points from the conversation:\n"
                "Only one turn in history."
            )
            self.assertEqual(result.strip(), expected_summary.strip())

if __name__ == '__main__':
    unittest.main()