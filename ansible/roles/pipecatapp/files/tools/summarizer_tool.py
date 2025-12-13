from sentence_transformers import SentenceTransformer, util

class SummarizerTool:
    """A tool to provide extractive summaries of the conversation.

    This tool uses a sentence embedding model to find and return the most
    relevant parts of the short-term conversation history based on a user's
    query. It does not generate new text (abstractive summary) but extracts
    existing conversational turns.

    Attributes:
        twin_service: A reference to the main TwinService instance to access memory.
        name (str): The name of the tool.
        description (str): A brief description of the tool's purpose.
        model: The SentenceTransformer model used for embeddings.
    """
    def __init__(self, twin_service=None):
        """Initializes the SummarizerTool.

        Args:
            twin_service: The instance of the main TwinService (optional).
        """
        self.twin_service = twin_service
        self.name = "summarizer"
        self.description = "A tool to provide summaries of the conversation."
        # Using a smaller, efficient model as requested.
        self.model = SentenceTransformer("google/embeddinggemma-300m")

    def get_summary(self, query: str, conversation_history: list = None) -> str:
        """Returns the most relevant parts of the conversation related to a query.

        This method performs extractive summarization. It embeds the user's query
        and all turns in the short-term memory, then uses cosine similarity to
        find the top 3 most relevant turns.

        Args:
            query (str): The topic or question to summarize the conversation around.
            conversation_history (list, optional): A list of conversation turns.
                If not provided, attempts to use twin_service.short_term_memory.

        Returns:
            str: A formatted string containing the most relevant conversational
                 turns, or a message if there is no history.
        """
        if conversation_history is None:
            if self.twin_service:
                conversation_history = self.twin_service.short_term_memory
            else:
                return "Error: No conversation history provided and no TwinService attached."

        if not conversation_history:
            return "There is no conversation history to summarize."

        # This tool performs extractive summarization by finding the most relevant
        # conversation turns for a given query, not abstractive summarization.

        # For optimal performance, EmbeddingGemma requires specific prefixes.
        query_with_prefix = "task: search result | query: " + query
        history_with_prefix = ["title: none | text: " + turn for turn in conversation_history]

        # Embed the query and the conversation history
        query_embedding = self.model.encode(query_with_prefix, convert_to_tensor=True)
        history_embeddings = self.model.encode(history_with_prefix, convert_to_tensor=True)

        # Compute cosine similarities
        similarities = util.cos_sim(query_embedding, history_embeddings)[0]

        # Get the top 3 most similar turns
        top_k = min(3, len(conversation_history))
        top_indices = similarities.topk(k=top_k).indices

        # Return the most relevant turns as the summary
        summary_lines = [conversation_history[i] for i in top_indices]
        summary = "\n".join(summary_lines)

        return f"Here are the most relevant points from the conversation:\n{summary}"
