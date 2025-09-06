from sentence_transformers import SentenceTransformer, util

class SummarizerTool:
    def __init__(self, twin_service):
        self.twin_service = twin_service
        self.name = "summarizer"
        self.description = "A tool to provide summaries of the conversation."
        # Using a smaller, efficient model as requested.
        self.model = SentenceTransformer("google/embeddinggemma-300m")

    def get_summary(self, query: str) -> str:
        """
        Returns the most relevant parts of the conversation related to a query.
        This is useful for getting a summary of a specific topic discussed.
        """
        conversation_history = self.twin_service.short_term_memory
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
