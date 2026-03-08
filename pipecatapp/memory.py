import faiss
import json
import sqlite3
from sentence_transformers import SentenceTransformer
import os
import logging
from cryptography.fernet import Fernet, InvalidToken

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
    def __init__(self, index_file="long_term_memory.faiss", store_file="long_term_memory.json", sqlite_file="long_term_memory.sqlite"):
        """Initializes the MemoryStore.

        Loads the embedding model and the existing memory files (or creates new
        ones if they don't exist). Also initializes the SQLite connection and schema.

        Args:
            index_file (str, optional): The filename for the FAISS index.
                Defaults to "long_term_memory.faiss".
            store_file (str, optional): The filename for the JSON text store.
                Defaults to "long_term_memory.json".
            sqlite_file (str, optional): The filename for the SQLite store.
                Defaults to "long_term_memory.sqlite".
        """
        # The embedding model is now managed by Ansible and placed in a predictable location.
        embedding_model_path = "/opt/nomad/models/embedding/bge-large-en-v1.5"
        self.embedding_model = SentenceTransformer(embedding_model_path)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        self.index_file = index_file
        self.store_file = store_file
        self.sqlite_file = sqlite_file

        encryption_key = os.getenv("MEMORY_ENCRYPTION_KEY")
        if encryption_key:
            try:
                self.fernet = Fernet(encryption_key.encode())
            except Exception as e:
                logging.error(f"Failed to initialize encryption with provided key. Invalid key format. App cannot start securely. Error: {e}")
                raise ValueError(f"Invalid MEMORY_ENCRYPTION_KEY provided: {e}")
        else:
            self.fernet = None

        self.index = self._load_index()
        self.store = self._load_store()
        self._init_sqlite()

    def _load_index(self):
        """Loads the FAISS index from disk or creates a new one."""
        if os.path.exists(self.index_file):
            return faiss.read_index(self.index_file)
        else:
            return faiss.IndexFlatL2(self.dimension)

    def _load_store(self):
        """Loads the text store from the JSON file or creates a new one, decrypting if necessary."""
        if os.path.exists(self.store_file):
            with open(self.store_file, 'r') as f:
                raw_store = json.load(f)

            store = {}
            for k, v in raw_store.items():
                if self.fernet:
                    if isinstance(v, str) and v.startswith("gAAAAA"):
                        try:
                            store[k] = self.fernet.decrypt(v.encode()).decode()
                        except InvalidToken:
                            logging.error(f"Failed to decrypt memory entry {k} with the current key. Data may be lost.")
                            # Cannot decrypt, keep as is so it doesn't get overwritten with corruption,
                            # or just leave it out? Best to keep raw to avoid data loss.
                            store[k] = v
                    else:
                        # It doesn't look like a Fernet token, assume legacy plaintext
                        store[k] = v
                else:
                    store[k] = v
            return store
        else:
            return {}

    def _save(self):
        """Saves the FAISS index and the text store to disk, encrypting if configured."""
        faiss.write_index(self.index, self.index_file)

        store_to_save = {}
        for k, v in self.store.items():
            if self.fernet:
                try:
                    store_to_save[k] = self.fernet.encrypt(v.encode()).decode()
                except Exception as e:
                    logging.error(f"Failed to encrypt memory entry {k}: {e}")
                    store_to_save[k] = v
            else:
                store_to_save[k] = v

        with open(self.store_file, 'w') as f:
            json.dump(store_to_save, f)

    def _init_sqlite(self):
        """Initializes the SQLite database and schema."""
        self.conn = sqlite3.connect(self.sqlite_file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                raw_text TEXT NOT NULL,
                summary TEXT,
                entities TEXT,
                topics TEXT,
                importance INTEGER,
                consolidated BOOLEAN DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consolidations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_ids TEXT NOT NULL,
                summary TEXT,
                insight TEXT
            )
        ''')
        self.conn.commit()

    def _encrypt(self, text: str) -> str:
        if self.fernet and text is not None:
            return self.fernet.encrypt(text.encode()).decode()
        return text

    def _decrypt(self, text: str) -> str:
        if self.fernet and text is not None:
            try:
                return self.fernet.decrypt(text.encode()).decode()
            except InvalidToken:
                logging.error("Failed to decrypt text with the current key. Data may be lost.")
                return text
        return text

    def add_memory(self, source: str, raw_text: str, summary: str = None, entities: list = None, topics: list = None, importance: int = None, consolidated: bool = False):
        """Adds a new memory to the SQLite store.

        Args:
            source (str): Source of the memory.
            raw_text (str): Raw text of the memory.
            summary (str, optional): Summary of the memory.
            entities (list, optional): List of entities extracted.
            topics (list, optional): List of topics covered.
            importance (int, optional): Importance score (e.g., 1-10).
            consolidated (bool, optional): Whether this memory is already consolidated. Defaults to False.

        Returns:
            int: The new memory's ID.
        """
        entities_str = json.dumps(entities) if entities is not None else None
        topics_str = json.dumps(topics) if topics is not None else None

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO memories (source, raw_text, summary, entities, topics, importance, consolidated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            source,
            self._encrypt(raw_text),
            self._encrypt(summary),
            self._encrypt(entities_str),
            self._encrypt(topics_str),
            importance,
            1 if consolidated else 0
        ))
        self.conn.commit()
        return cursor.lastrowid

    def add_consolidation(self, source_ids: list, summary: str, insight: str = None):
        """Adds a new consolidation to the SQLite store.

        Args:
            source_ids (list): List of memory IDs this consolidation is based on.
            summary (str): Summary of the consolidated memories.
            insight (str, optional): Insight generated from the consolidation.

        Returns:
            int: The new consolidation's ID.
        """
        source_ids_str = json.dumps(source_ids)

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO consolidations (source_ids, summary, insight)
            VALUES (?, ?, ?)
        ''', (
            source_ids_str,
            self._encrypt(summary),
            self._encrypt(insight)
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_unconsolidated_memories(self, limit: int = 10) -> list[dict]:
        """Fetches a list of unconsolidated memories from the SQLite store.

        Args:
            limit (int, optional): Maximum number of memories to return. Defaults to 10.

        Returns:
            list[dict]: A list of memory dictionaries.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM memories WHERE consolidated = 0 LIMIT ?', (limit,))
        rows = cursor.fetchall()

        memories = []
        for row in rows:
            memory = dict(row)
            memory['raw_text'] = self._decrypt(memory['raw_text'])
            memory['summary'] = self._decrypt(memory['summary'])

            entities_str = self._decrypt(memory['entities'])
            memory['entities'] = json.loads(entities_str) if entities_str else None

            topics_str = self._decrypt(memory['topics'])
            memory['topics'] = json.loads(topics_str) if topics_str else None

            memory['consolidated'] = bool(memory['consolidated'])
            memories.append(memory)

        return memories

    def get_memory(self, memory_id: int) -> dict:
        """Fetches a single memory by ID.

        Args:
            memory_id (int): The ID of the memory.

        Returns:
            dict: The memory dictionary, or None if not found.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM memories WHERE id = ?', (memory_id,))
        row = cursor.fetchone()

        if row:
            memory = dict(row)
            memory['raw_text'] = self._decrypt(memory['raw_text'])
            memory['summary'] = self._decrypt(memory['summary'])

            entities_str = self._decrypt(memory['entities'])
            memory['entities'] = json.loads(entities_str) if entities_str else None

            topics_str = self._decrypt(memory['topics'])
            memory['topics'] = json.loads(topics_str) if topics_str else None

            memory['consolidated'] = bool(memory['consolidated'])
            return memory
        return None

    def get_consolidation(self, consolidation_id: int) -> dict:
        """Fetches a single consolidation by ID.

        Args:
            consolidation_id (int): The ID of the consolidation.

        Returns:
            dict: The consolidation dictionary, or None if not found.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM consolidations WHERE id = ?', (consolidation_id,))
        row = cursor.fetchone()

        if row:
            consolidation = dict(row)
            consolidation['source_ids'] = json.loads(consolidation['source_ids'])
            consolidation['summary'] = self._decrypt(consolidation['summary'])
            consolidation['insight'] = self._decrypt(consolidation['insight'])
            return consolidation
        return None

    def mark_memory_consolidated(self, memory_id: int):
        """Marks a memory as consolidated.

        Args:
            memory_id (int): The ID of the memory to mark.
        """
        cursor = self.conn.cursor()
        cursor.execute('UPDATE memories SET consolidated = 1 WHERE id = ?', (memory_id,))
        self.conn.commit()

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
