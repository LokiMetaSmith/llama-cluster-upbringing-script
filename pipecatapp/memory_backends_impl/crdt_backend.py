import uuid
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Fallback basic CRDT ORSet if liminal_bridge not found
class BasicORSet:
    def __init__(self):
        self.added = set()
        self.removed = set()

    def add(self, item: Any):
        u = str(uuid.uuid4())
        # We need a stable representation. Let's serialize dicts to json strings to hash them
        if isinstance(item, dict):
            item_hashable = json.dumps(item, sort_keys=True)
        else:
            item_hashable = str(item)
        self.added.add((item_hashable, u))

    def remove(self, item: Any):
        if isinstance(item, dict):
            item_hashable = json.dumps(item, sort_keys=True)
        else:
            item_hashable = str(item)
        to_remove = [x for x in self.added if x[0] == item_hashable and x not in self.removed]
        self.removed.update(to_remove)

    def merge(self, other: "BasicORSet"):
        self.added.update(other.added)
        self.removed.update(other.removed)

    def value(self) -> List[Any]:
        items = {item[0] for item in self.added if item not in self.removed}
        res = []
        for i in items:
            try:
                res.append(json.loads(i))
            except Exception:
                res.append(i)
        return res

    def get_state(self):
        return {
            "added": list(self.added),
            "removed": list(self.removed)
        }

    def merge_state(self, state):
        self.added.update([tuple(x) for x in state["added"]])
        self.removed.update([tuple(x) for x in state["removed"]])


class CRDTMemoryBackend:
    """
    A prototype CRDT-based memory backend to enable seamless failover
    if a Nomad node crashes, tracking active agent conversation state.
    """
    def __init__(self, node_id: str = None):
        self.node_id = node_id or str(uuid.uuid4())
        self.doc = BasicORSet()

    def add(self, text: str):
        doc_id = str(uuid.uuid4())
        self.doc.add({"id": doc_id, "content": text, "metadata": {"node_id": self.node_id}})
        logger.info(f"CRDT Node {self.node_id} added document {doc_id}")

    def query(self, text: str, top_k: int = 5) -> List[str]:
        values = self.doc.value()
        results = []
        for val in values:
            if isinstance(val, dict) and "content" in val:
                if text.lower() in val["content"].lower():
                    results.append(val["content"])
        return results[:top_k]

    def reset(self):
        self.doc = BasicORSet()

    def get_timeline(self) -> List[Dict[str, Any]]:
        return [{"event": "crdt_init", "node_id": self.node_id}]

    def append_timeline_event(self, event_type: str, data: Dict[str, Any]):
        pass

    def save_skill(self, name: str, description: str, instructions: str):
        doc_id = f"skill_{name}"
        self.doc.add({"id": doc_id, "content": instructions, "metadata": {"type": "skill", "description": description}})

    def get_skill(self, name: str) -> Optional[dict]:
        doc_id = f"skill_{name}"
        values = self.doc.value()
        for val in values:
            if isinstance(val, dict) and val.get("id") == doc_id:
                return {"name": name, "description": val["metadata"].get("description", ""), "instructions": val["content"]}
        return None

    def list_skills(self) -> List[dict]:
        skills = []
        values = self.doc.value()
        for val in values:
            if isinstance(val, dict) and val.get("metadata", {}).get("type") == "skill":
                 skills.append({"name": val["id"].replace("skill_", ""), "description": val["metadata"].get("description", "")})
        return skills

    def delete_skill(self, name: str) -> bool:
        doc_id = f"skill_{name}"
        values = self.doc.value()
        found = False
        for val in values:
            if isinstance(val, dict) and val.get("id") == doc_id:
                self.doc.remove(val)
                found = True
        return found

    def write_documents(self, documents: List[Any]) -> int:
        for d in documents:
            if hasattr(d, "to_dict"):
                self.doc.add(d.to_dict())
            else:
                self.doc.add(d)
        return len(documents)

    def filter_documents(self, filters: Dict[str, Any] = None) -> List[Any]:
        from pipecatapp.memory import Document
        docs_list = []
        values = self.doc.value()
        for val in values:
            if isinstance(val, dict) and "id" in val:
                docs_list.append(Document(id=val["id"], content=val.get("content", ""), metadata=val.get("metadata", {})))
        return docs_list

    # CRDT specific methods
    def merge(self, state: Dict[str, Any]):
        """Merges remote CRDT state into local state."""
        self.doc.merge_state(state)
        logger.info(f"CRDT Node {self.node_id} merged state.")

    def get_state(self) -> Dict[str, Any]:
        """Returns the current state for gossiping to other nodes."""
        return self.doc.get_state()
