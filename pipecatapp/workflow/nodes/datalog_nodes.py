"""DatalogStateNode for declarative workflow engine in PipecatApp.
"""

from typing import Dict, Any
from pipecatapp.workflow.nodes.registry import registry
from pipecatapp.datalog_memory import DatalogMemory

try:
    from pipecatapp.workflow.nodes.base_nodes import Node
except ImportError:
    from .base_nodes import Node

@registry.register
class DatalogStateNode(Node):
    """Workflow node for querying, asserting, retracting, and explaining Datalog maintained state."""

    name = "DatalogStateNode"
    description = "Queries, asserts, retracts, or explains facts in the Datalog maintained state memory."

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.action = config.get("action", "query")  # query, assert, retract, explain, hybrid
        self.predicate = config.get("predicate")
        self.args = config.get("args", [])
        self.query_text = config.get("query_text", "")
        self.datalog_memory = config.get("datalog_memory") or DatalogMemory()

    def execute(self, context) -> Dict[str, Any]:
        """Executes the Datalog state action."""
        if self.action == "assert":
            if not self.predicate:
                return {"status": "error", "error": "predicate is required for assert action"}
            rec = self.datalog_memory.assert_fact(self.predicate, *self.args)
            return {"status": "success", "fact": repr(rec)}

        elif self.action == "retract":
            if not self.predicate:
                return {"status": "error", "error": "predicate is required for retract action"}
            success = self.datalog_memory.retract_fact(self.predicate, *self.args)
            return {"status": "success", "retracted": success}

        elif self.action == "explain":
            if not self.predicate:
                return {"status": "error", "error": "predicate is required for explain action"}
            explanation = self.datalog_memory.explain(self.predicate, *self.args)
            return {"status": "success", "explanation": explanation}

        elif self.action == "hybrid":
            results = self.datalog_memory.query_hybrid(self.query_text)
            return {"status": "success", "results": results}

        else:  # default query
            facts = self.datalog_memory.query_state(predicate=self.predicate)
            return {"status": "success", "facts": facts}
