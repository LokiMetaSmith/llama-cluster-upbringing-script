import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os

class MemoryStore:
    def __init__(self, index_file="long_term_memory.faiss", store_file="long_term_memory.json"):
        embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME", 'all-MiniLM-L6-v2')
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        self.index_file = index_file
        self.store_file = store_file
        self.index = self._load_index()
        self.store = self._load_store()

    def _load_index(self):
        if os.path.exists(self.index_file):
            return faiss.read_index(self.index_file)
        else:
            return faiss.IndexFlatL2(self.dimension)

    def _load_store(self):
        if os.path.exists(self.store_file):
            with open(self.store_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def _save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.store_file, 'w') as f:
            json.dump(self.store, f)

    def add(self, text):
        embedding = self.embedding_model.encode([text])
        new_id = self.index.ntotal
        self.index.add(embedding)
        self.store[str(new_id)] = text
        self._save()

    def search(self, query_text, k=3):
        if self.index.ntotal == 0:
            return []

        query_embedding = self.embedding_model.encode([query_text])
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for i in indices[0]:
            if i != -1:
                results.append(self.store.get(str(i)))

        return results
