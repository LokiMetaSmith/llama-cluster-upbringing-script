import os
import json
import uuid
import base64
import logging
from typing import List, Dict, Any, Optional
import httpx
from pipecatapp.memory_backends import BaseMemoryBackend

logger = logging.getLogger(__name__)

class ConsulMemoryBackend(BaseMemoryBackend):
    """
    A stateless memory backend that persists all state directly into the Consul KV store.
    This prevents memory bloat on constrained nodes and ensures seamless failovers.
    """
    def __init__(self, prefix: str = "pipecat/memory/"):
        self.consul_url = os.getenv("CONSUL_HTTP_ADDR", "http://127.0.0.1:8500")
        if not self.consul_url.startswith("http"):
            self.consul_url = "http://" + self.consul_url
        self.prefix = prefix
        self.client = httpx.Client(base_url=self.consul_url)

    def _put_kv(self, key: str, value: Any):
        try:
            val_str = json.dumps(value) if not isinstance(value, str) else value
            res = self.client.put(f"/v1/kv/{self.prefix}{key}", content=val_str)
            res.raise_for_status()
        except Exception as e:
            logger.error(f"Consul KV PUT failed for {key}: {e}")

    def _get_kv(self, key: str) -> Optional[Any]:
        try:
            res = self.client.get(f"/v1/kv/{self.prefix}{key}")
            if res.status_code == 404:
                return None
            res.raise_for_status()
            data = res.json()
            if data and isinstance(data, list) and len(data) > 0:
                raw_val = base64.b64decode(data[0].get("Value", "")).decode("utf-8")
                try:
                    return json.loads(raw_val)
                except json.JSONDecodeError:
                    return raw_val
            return None
        except Exception as e:
            logger.error(f"Consul KV GET failed for {key}: {e}")
            return None

    def _delete_kv(self, key: str) -> bool:
        try:
            res = self.client.delete(f"/v1/kv/{self.prefix}{key}")
            res.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Consul KV DELETE failed for {key}: {e}")
            return False

    def _list_kv(self, sub_prefix: str = "") -> List[Dict[str, Any]]:
        try:
            res = self.client.get(f"/v1/kv/{self.prefix}{sub_prefix}?recurse=true")
            if res.status_code == 404:
                return []
            res.raise_for_status()
            results = []
            for item in res.json():
                try:
                    val = base64.b64decode(item.get("Value", "")).decode("utf-8")
                    results.append({"Key": item["Key"], "Value": json.loads(val)})
                except Exception:
                    pass
            return results
        except Exception as e:
            logger.error(f"Consul KV LIST failed for {sub_prefix}: {e}")
            return []

    def add(self, text: str):
        doc_id = str(uuid.uuid4())
        self._put_kv(f"docs/{doc_id}", {"content": text})

    def force_save(self):
        # Consul writes are synchronous and persistent immediately.
        pass

    def search(self, query_text: str, k: int = 3) -> List[str]:
        # Naive keyword search over all docs for PoC/legacy fallback
        results = []
        docs = self._list_kv("docs/")
        for doc in docs:
            content = doc["Value"].get("content", "")
            if query_text.lower() in content.lower():
                results.append(content)
        return results[:k]

    def add_memory(self, source: str, raw_text: str, summary: str | None = None, entities: list | None = None, topics: list | None = None, importance: int | None = None, consolidated: bool = False, metadata: dict | None = None, doc_id: str | None = None):
        mem_id = doc_id or str(uuid.uuid4())
        self._put_kv(f"memories/{mem_id}", {
            "source": source,
            "raw_text": raw_text,
            "summary": summary,
            "metadata": metadata or {},
            "consolidated": consolidated
        })

    def get_memory(self, memory_id: int) -> Optional[dict]:
        return self._get_kv(f"memories/{memory_id}")

    def get_unconsolidated_memories(self, limit: int = 50) -> List[dict]:
        results = []
        mems = self._list_kv("memories/")
        for mem in mems:
            if not mem["Value"].get("consolidated", False):
                results.append(mem["Value"])
                if len(results) >= limit:
                    break
        return results

    def add_consolidation(self, source_ids: List[int], summary: str, insight: str | None = None) -> int:
        cons_id = str(uuid.uuid4())
        self._put_kv(f"consolidations/{cons_id}", {
            "source_ids": source_ids,
            "summary": summary,
            "insight": insight
        })
        return cons_id

    def get_consolidation(self, consolidation_id: int) -> Optional[dict]:
        return self._get_kv(f"consolidations/{consolidation_id}")

    def mark_memory_consolidated(self, memory_id: int):
        mem = self.get_memory(memory_id)
        if mem:
            mem["consolidated"] = True
            self._put_kv(f"memories/{memory_id}", mem)

    def add_activity(self, activity_type: str, description: str, metadata: dict | None = None) -> int:
        act_id = str(uuid.uuid4())
        self._put_kv(f"activities/{act_id}", {
            "activity_type": activity_type,
            "description": description,
            "metadata": metadata or {}
        })
        return act_id

    def get_activities(self, limit: int = 50) -> List[dict]:
        acts = self._list_kv("activities/")
        return [a["Value"] for a in acts][:limit]

    def save_skill(self, name: str, description: str, content: str) -> None:
        self._put_kv(f"skills/{name}", {
            "name": name,
            "description": description,
            "content": content
        })

    def get_skill(self, name: str) -> Optional[dict]:
        return self._get_kv(f"skills/{name}")

    def list_skills(self) -> List[dict]:
        skills = self._list_kv("skills/")
        return [{"name": s["Value"].get("name"), "description": s["Value"].get("description")} for s in skills]

    def delete_skill(self, name: str) -> bool:
        return self._delete_kv(f"skills/{name}")

    def write_documents(self, documents: List[Any]) -> int:
        for doc in documents:
            doc_dict = doc.to_dict() if hasattr(doc, "to_dict") else doc
            self._put_kv(f"docs/{doc_dict.get('id', str(uuid.uuid4()))}", doc_dict)
        return len(documents)

    def filter_documents(self, filters: Dict[str, Any] = None) -> List[Any]:
        from pipecatapp.memory import Document
        results = []
        docs = self._list_kv("docs/")
        for doc in docs:
            val = doc["Value"]
            # basic filtering mock
            match = True
            if filters:
                for k, v in filters.items():
                    if val.get("metadata", {}).get(k) != v:
                        match = False
                        break
            if match:
                results.append(Document(id=val.get("id"), content=val.get("content", ""), metadata=val.get("metadata", {})))
        return results
