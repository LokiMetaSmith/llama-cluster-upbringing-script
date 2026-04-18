from typing import Any, List
from ..node import Node
from .registry import registry
from ..context import WorkflowContext
try:
    from ...memory import Document, MemoryStore
except ImportError:
    from memory import Document, MemoryStore

@registry.register
class TextSplitterNode(Node):
    """
    Splits a single large text string into multiple smaller Document objects
    based on a defined chunk size, keeping metadata intact.
    """
    def __init__(self, config):
        super().__init__(config)
        self.expected_inputs = {"raw_text", "metadata"}
        self.expected_outputs = {"documents"}
        self.chunk_size = config.get("config", {}).get("chunk_size", 1000)
        self.chunk_overlap = config.get("config", {}).get("chunk_overlap", 100)

    async def execute(self, context: WorkflowContext):
        raw_text = self.get_input(context, "raw_text")

        try:
            metadata = self.get_input(context, "metadata")
        except ValueError:
            metadata = {}

        if not raw_text:
            self.set_output(context, "documents", [])
            return

        # Basic character-based overlapping chunker
        chunks = []
        start = 0
        text_len = len(raw_text)

        while start < text_len:
            end = start + self.chunk_size
            chunk = raw_text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap

        docs = [Document(content=chunk, metadata=metadata) for chunk in chunks]
        self.set_output(context, "documents", docs)

@registry.register
class DocumentWriterNode(Node):
    """
    Takes a list of Haystack-style Document objects and writes them
    to the shared MemoryStore vector database.
    """
    def __init__(self, config):
        super().__init__(config)
        self.expected_inputs = {"documents"}
        self.expected_outputs = {"write_count"}

    async def execute(self, context: WorkflowContext):
        documents = self.get_input(context, "documents")

        if not documents:
             self.set_output(context, "write_count", 0)
             return

        # Extract MemoryStore from global context if injected, otherwise instantiate (less ideal)
        memory_store = context.global_inputs.get("memory_store")

        if not memory_store:
            # Fallback initialization
            memory_store = MemoryStore()

        count = memory_store.write_documents(documents)
        self.set_output(context, "write_count", count)
