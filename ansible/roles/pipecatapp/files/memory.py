import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os

class MemoryStore:
    """Manages the agent's long-term memory using a vector database.

    This class handles the storage and retrieval of textual memories. It uses a
    SentenceTransformer model to create vector embeddings of text, a FAISS index
    for efficient similarity searching, and a JSON file to store the actual
    text content.

    Attributes:
        embedding_model: The SentenceTransformer model for creating embeddings.
        dimension (int): The dimensionality of the embeddings.
        index_file (str): The path to the FAISS index file.
        store_file (str): The path to the JSON file for text storage.
        index: The loaded FAISS index.
        store (dict): A dictionary mapping index IDs to text.
    """
    def __init__(self, index_file="long_term_memory.faiss", store_file="long_term_memory.json"):
        """Initializes the MemoryStore.

        Loads the embedding model and the existing memory files (or creates new
        ones if they don't exist).

        Args:
            index_file (str, optional): The filename for the FAISS index.
                Defaults to "long_term_memory.faiss".
            store_file (str, optional): The filename for the JSON text store.
                Defaults to "long_term_memory.json".
        """
        # The embedding model is now managed by Ansible and placed in a predictable location.
        embedding_model_path = "/opt/nomad/models/embedding/bge-large-en-v1.5"
        self.embedding_model = SentenceTransformer(embedding_model_path)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        self.index_file = index_file
        self.store_file = store_file
        self.index = self._load_index()
        self.store = self._load_store()

    def _load_index(self):
        """Loads the FAISS index from disk or creates a new one."""
        if os.path.exists(self.index_file):
            return faiss.read_index(self.index_file)
        else:
            return faiss.IndexFlatL2(self.dimension)

    def _load_store(self):
        """Loads the text store from the JSON file or creates a new one."""
        if os.path.exists(self.store_file):
            with open(self.store_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def _save(self):
        """Saves the FAISS index and the text store to disk."""
        faiss.write_index(self.index, self.index_file)
        with open(self.store_file, 'w') as f:
            json.dump(self.store, f)

    def add(self, text: str):
        """Adds a new text entry to the memory.

        The text is encoded into a vector, added to the FAISS index, and the
        original text is saved in the store.

        Args:
            text (str): The text to add to the memory.
        """
        embedding = self.embedding_model.encode([text])
        new_id = self.index.ntotal
        self.index.add(embedding)
        self.store[str(new_id)] = text
        self._save()

    def search(self, query_text: str, k: int = 3) -> list[str]:
        """Searches the memory for the most relevant entries.

        Encodes the query text and uses the FAISS index to find the `k` most
        similar text entries.

        Args:
            query_text (str): The text to search for.
            k (int, optional): The number of results to return. Defaults to 3.

        Returns:
            list[str]: A list of the most relevant text entries found.
        """
        if self.index.ntotal == 0:
            return []

        query_embedding = self.embedding_model.encode([query_text])
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for i in indices[0]:
            if i != -1:
                results.append(self.store.get(str(i)))

        return results
