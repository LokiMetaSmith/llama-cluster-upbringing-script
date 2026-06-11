import os
import uuid
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pipecatapp.memory_legacy import MemoryStore as LegacyMemoryStore
from pipecatapp.memory_backends_impl.helix_backend import HelixMemoryBackend

@dataclass
class Document:
    """Standardized Haystack-style Document Protocol for Pipecat memory."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {"id": self.id, "content": self.content, "metadata": self.metadata}

class MemoryStore:
    def __init__(self, index_file="long_term_memory.faiss", store_file="long_term_memory.json", sqlite_file="long_term_memory.sqlite"):
        self.use_helix = os.getenv("USE_HELIX_MEMORY", "false").lower() == "true"

        if self.use_helix:
            logging.info("Initializing HelixDB Memory Backend...")
            self.backend = HelixMemoryBackend()
        else:
            logging.info("Initializing Legacy FAISS+SQLite Memory Backend...")
            self.backend = LegacyMemoryStore(index_file=index_file, store_file=store_file, sqlite_file=sqlite_file)

    def add(self, text: str):
        self.backend.add(text)

    def force_save(self):
        self.backend.force_save()

    def search(self, query_text: str, k: int = 3) -> List[str]:
        return self.backend.search(query_text, k)

    def add_memory(self, source: str, raw_text: str, summary: str = None, entities: list = None, topics: list = None, importance: int = None, consolidated: bool = False, metadata: dict = None, doc_id: str = None):
        self.backend.add_memory(source, raw_text, summary, entities, topics, importance, consolidated, metadata, doc_id)

    def get_memory(self, memory_id: int) -> Optional[dict]:
        return self.backend.get_memory(memory_id)

    def get_unconsolidated_memories(self, limit: int = 50) -> List[dict]:
        return self.backend.get_unconsolidated_memories(limit)

    def add_consolidation(self, source_ids: List[int], summary: str, insight: str = None) -> int:
        return self.backend.add_consolidation(source_ids, summary, insight)

    def get_consolidation(self, consolidation_id: int) -> Optional[dict]:
        return self.backend.get_consolidation(consolidation_id)

    def mark_memory_consolidated(self, memory_id: int):
        self.backend.mark_memory_consolidated(memory_id)

    def add_activity(self, activity_type: str, description: str, metadata: dict = None) -> int:
        return self.backend.add_activity(activity_type, description, metadata)

    def get_activities(self, limit: int = 50) -> List[dict]:
        return self.backend.get_activities(limit)

    def save_skill(self, name: str, description: str, content: str) -> None:
        self.backend.save_skill(name, description, content)

    def get_skill(self, name: str) -> Optional[dict]:
        return self.backend.get_skill(name)

    def list_skills(self) -> List[dict]:
        return self.backend.list_skills()

    def delete_skill(self, name: str) -> bool:
        return self.backend.delete_skill(name)

    def write_documents(self, documents: List[Document]) -> int:
        if self.use_helix:
             # Basic implementation for PoC using add
             for doc in documents:
                  meta_str = ", ".join(f"{k}: {v}" for k, v in doc.metadata.items())
                  full_text = f"[{meta_str}] {doc.content}" if meta_str else doc.content
                  self.add(full_text)
             return len(documents)
        else:
             return self.backend.write_documents(documents)

    def filter_documents(self, filters: Dict[str, Any] = None) -> List[Document]:
        if self.use_helix:
             return []
        else:
             return self.backend.filter_documents(filters)
