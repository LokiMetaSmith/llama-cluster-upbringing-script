import json
import logging
from typing import List, Dict, Any, Optional
from pipecatapp.memory_backends import BaseMemoryBackend
from pipecatapp.memory_backends_impl.helix_client import HelixClient

logger = logging.getLogger(__name__)

class HelixMemoryBackend(BaseMemoryBackend):
    def __init__(self):
        self.client = HelixClient()

    def add(self, text: str):
        query = {
            "Query": {
                "name": "mem",
                "steps": [
                    {
                        "AddN": {
                            "label": "Document",
                            "properties": [
                                ["text", {"Value": {"String": text}}],
                                ["type", {"Value": {"String": "faiss_compat"}}]
                            ]
                        }
                    },
                    {
                        "Project": [{"source": "text", "alias": "text"}]
                    }
                ],
                "condition": None
            }
        }
        self.client.execute_ast(queries=[query], returns=["mem"])

    def force_save(self):
        pass

    def search(self, query_text: str, k: int = 3) -> List[str]:
        query = {
            "Query": {
                "name": "results",
                "steps": [
                    {
                        "NWithLabel": {"label": "Document"}
                    },
                    {
                         "Project": [{"source": "text", "alias": "text"}]
                    }
                ],
                "condition": None
            }
        }
        res = self.client.execute_ast(queries=[query], returns=["results"], request_type="read")
        results = []
        if res and "results" in res:
             for r in res["results"]:
                 if isinstance(r, dict) and "text" in r:
                     results.append(r["text"])
        return results[:k]

    def add_memory(self, source: str, raw_text: str, summary: str = None, entities: list = None, topics: list = None, importance: int = None, consolidated: bool = False, metadata: dict = None, doc_id: str = None):
         meta_str = json.dumps(metadata) if metadata else "{}"
         query = {
             "Query": {
                 "name": "mem",
                 "steps": [
                     {
                         "AddN": {
                             "label": "Memory",
                             "properties": [
                                 ["source", {"Value": {"String": source}}],
                                 ["raw_text", {"Value": {"String": raw_text}}],
                                 ["summary", {"Value": {"String": summary or ""}}],
                                 ["metadata", {"Value": {"String": meta_str}}],
                                 ["doc_id", {"Value": {"String": doc_id or ""}}]
                             ]
                         }
                     },
                     {"Project": [{"source": "raw_text", "alias": "raw_text"}]}
                 ],
                 "condition": None
             }
         }
         self.client.execute_ast(queries=[query], returns=["mem"])

    def get_memory(self, memory_id: int) -> Optional[dict]:
         raise NotImplementedError("PoC limitation: Retrieving memories by ID not fully supported in Helix backend yet.")

    def get_unconsolidated_memories(self, limit: int = 50) -> List[dict]:
         raise NotImplementedError("PoC limitation: Unconsolidated memories not fully supported in Helix backend yet.")

    def add_consolidation(self, source_ids: List[int], summary: str, insight: str = None) -> int:
         raise NotImplementedError("PoC limitation: Consolidations not supported in Helix backend yet.")

    def get_consolidation(self, consolidation_id: int) -> Optional[dict]:
         raise NotImplementedError("PoC limitation: Consolidations not supported in Helix backend yet.")

    def mark_memory_consolidated(self, memory_id: int):
         raise NotImplementedError("PoC limitation: Consolidations not supported in Helix backend yet.")

    def add_activity(self, activity_type: str, description: str, metadata: dict = None) -> int:
         raise NotImplementedError("PoC limitation: Activity timeline not supported in Helix backend yet.")

    def get_activities(self, limit: int = 50) -> List[dict]:
         raise NotImplementedError("PoC limitation: Activity timeline not supported in Helix backend yet.")

    def save_skill(self, name: str, description: str, content: str) -> None:
         query = {
             "Query": {
                 "name": "skill",
                 "steps": [
                     {
                         "AddN": {
                             "label": "DynamicSkill",
                             "properties": [
                                 ["name", {"Value": {"String": name}}],
                                 ["description", {"Value": {"String": description}}],
                                 ["content", {"Value": {"String": content}}],
                                 ["version", {"Value": {"Int": 1}}]
                             ]
                         }
                     },
                     {"Project": [{"source": "name", "alias": "name"}]}
                 ],
                 "condition": None
             }
         }
         self.client.execute_ast(queries=[query], returns=["skill"])

    def get_skill(self, name: str) -> Optional[dict]:
         raise NotImplementedError("PoC limitation: Reading dynamic skills not supported in Helix backend yet.")

    def list_skills(self) -> List[dict]:
         raise NotImplementedError("PoC limitation: Listing dynamic skills not supported in Helix backend yet.")

    def delete_skill(self, name: str) -> bool:
         raise NotImplementedError("PoC limitation: Deleting dynamic skills not supported in Helix backend yet.")
