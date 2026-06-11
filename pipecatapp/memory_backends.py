from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseMemoryBackend(ABC):
    """Abstract interface for memory backends."""

    @abstractmethod
    def add(self, text: str):
        pass

    @abstractmethod
    def force_save(self):
        pass

    @abstractmethod
    def search(self, query_text: str, k: int = 3) -> List[str]:
        pass

    @abstractmethod
    def add_memory(self, source: str, raw_text: str, summary: str = None, entities: list = None, topics: list = None, importance: int = None, consolidated: bool = False, metadata: dict = None, doc_id: str = None):
        pass

    @abstractmethod
    def get_memory(self, memory_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    def get_unconsolidated_memories(self, limit: int = 50) -> List[dict]:
        pass

    @abstractmethod
    def add_consolidation(self, source_ids: List[int], summary: str, insight: str = None) -> int:
        pass

    @abstractmethod
    def get_consolidation(self, consolidation_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    def mark_memory_consolidated(self, memory_id: int):
        pass

    @abstractmethod
    def add_activity(self, activity_type: str, description: str, metadata: dict = None) -> int:
        pass

    @abstractmethod
    def get_activities(self, limit: int = 50) -> List[dict]:
        pass

    @abstractmethod
    def save_skill(self, name: str, description: str, content: str) -> None:
        pass

    @abstractmethod
    def get_skill(self, name: str) -> Optional[dict]:
        pass

    @abstractmethod
    def list_skills(self) -> List[dict]:
        pass

    @abstractmethod
    def delete_skill(self, name: str) -> bool:
        pass
