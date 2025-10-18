import chromadb
import uuid
import os

class MemoryStore:
    """Manages the agent's long-term memory using a ChromaDB service.

    This class handles the storage and retrieval of textual memories. It connects
    to a remote ChromaDB instance to manage different collections of memories,
    such as conversational history and RAG documents.

    Attributes:
        client: The ChromaDB client instance.
        conversational_memory: The collection for storing conversational snippets.
    """
    def __init__(self, host="localhost", port=8000):
        """Initializes the MemoryStore.

        Connects to the ChromaDB service and gets or creates the necessary
        collections.

        Args:
            host (str, optional): The hostname of the ChromaDB service.
                Defaults to "localhost".
            port (int, optional): The port of the ChromaDB service.
                Defaults to 8000.
        """
        self.client = chromadb.HttpClient(host=host, port=port)
        # The embedding model is now managed by ChromaDB, but we can still specify
        # a model when creating a collection if needed. For now, we rely on the
        # default embedding function configured in ChromaDB.
        self.conversational_memory = self.client.get_or_create_collection(
            name="conversations"
        )

    def add(self, text: str, metadata: dict = None):
        """Adds a new text entry to the conversational memory.

        Args:
            text (str): The text to add to the memory.
            metadata (dict, optional): A dictionary of metadata to store alongside
                the text. Defaults to None.
        """
        # ChromaDB requires a unique ID for each document.
        doc_id = str(uuid.uuid4())
        self.conversational_memory.add(
            documents=[text],
            metadatas=[metadata] if metadata else [{}],
            ids=[doc_id]
        )

    def search(self, query_text: str, k: int = 3, collection_name: str = "conversations") -> list[str]:
        """Searches a specified memory collection for the most relevant entries.

        Args:
            query_text (str): The text to search for.
            k (int, optional): The number of results to return. Defaults to 3.
            collection_name (str, optional): The name of the collection to search.
                Defaults to "conversations".

        Returns:
            list[str]: A list of the most relevant text entries found.
        """
        collection = self.client.get_collection(name=collection_name)
        if collection.count() == 0:
            return []

        results = collection.query(
            query_texts=[query_text],
            n_results=k
        )
        # The results are in a list of lists, we care about the first query's results
        return results['documents'][0]