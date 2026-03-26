from typing import Any, Iterable, List, Optional
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document

from pmm_memory import PMMMemory
from memory import MemoryStore


class PMMChatMessageHistory(BaseChatMessageHistory):
    """
    A LangChain BaseChatMessageHistory wrapper for the custom PMMMemory
    event-sourced ledger. It reads and writes to the SQLite database.
    """
    def __init__(self, pmm_memory: PMMMemory, session_id: str = "default"):
        self.pmm_memory = pmm_memory
        self.session_id = session_id

    @property
    def messages(self) -> List[BaseMessage]:
        """Fetch messages from the PMM ledger."""
        # Get recent events from PMM. By default, it retrieves the last 50
        # messages to keep the context window manageable.
        events = self.pmm_memory.get_events_sync(limit=50)

        langchain_messages = []
        for event in events:
            # PMM events are ordered oldest to newest from get_events_sync
            # Wait, get_events_sync returns list(reversed(events)) which means
            # it IS oldest to newest. Good.

            # Optionally filter by session_id if stored in meta
            if event["meta"].get("session_id", "default") != self.session_id:
                 continue

            kind = event["kind"]
            content = event["content"]

            if kind == "user_message":
                langchain_messages.append(HumanMessage(content=content))
            elif kind == "assistant_message":
                langchain_messages.append(AIMessage(content=content))
            elif kind == "system_message":
                langchain_messages.append(SystemMessage(content=content))

        return langchain_messages

    def add_message(self, message: BaseMessage) -> None:
        """Add a LangChain message to the PMM ledger."""
        meta = {"session_id": self.session_id}

        if isinstance(message, HumanMessage):
             self.pmm_memory.add_event_sync(kind="user_message", content=message.content, meta=meta)
        elif isinstance(message, AIMessage):
             self.pmm_memory.add_event_sync(kind="assistant_message", content=message.content, meta=meta)
        elif isinstance(message, SystemMessage):
             self.pmm_memory.add_event_sync(kind="system_message", content=message.content, meta=meta)
        else:
             # Fallback for unknown message types
             self.pmm_memory.add_event_sync(kind="generic_message", content=message.content, meta=meta)

    def clear(self) -> None:
        """
        Clearing the ledger is not supported in an event-sourced architecture.
        We could potentially add a 'clear_session' event, but for now we ignore.
        """
        pass


class PipecatVectorStore(VectorStore):
    """
    A LangChain VectorStore wrapper for the custom MemoryStore (FAISS/SQLite)
    implemented in memory.py.
    """
    def __init__(self, memory_store: MemoryStore):
        self.memory_store = memory_store

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> List[str]:
        """Run more texts through the embeddings and add to the vectorstore."""
        ids = []
        for i, text in enumerate(texts):
            # In memory.py, .add() takes a string and adds to FAISS and JSON store
            self.memory_store.add(text)

            # Since memory.py doesn't return the ID, we have to calculate it based on ntotal
            # or we could add it to SQLite if metadatas are provided
            if metadatas and len(metadatas) > i:
                 metadata = metadatas[i]
                 # Save structured metadata to the SQLite side of memory.py
                 self.memory_store.add_memory(
                     source=metadata.get("source", "unknown"),
                     raw_text=text,
                     summary=metadata.get("summary"),
                     entities=metadata.get("entities"),
                     topics=metadata.get("topics")
                 )
            ids.append(str(self.memory_store.index.ntotal - 1))
        return ids

    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        """Return docs most similar to query."""
        results = self.memory_store.search(query, k=k)

        documents = []
        for res in results:
             if res:
                 documents.append(Document(page_content=res))

        return documents

    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Any,
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> "PipecatVectorStore":
        """
        Not implemented because PipecatVectorStore initializes its own
        SentenceTransformer via MemoryStore.
        """
        raise NotImplementedError("Use the PipecatVectorStore constructor directly with an existing MemoryStore.")
