import pytest
from unittest.mock import MagicMock, patch

from pipecatapp.langchain_memory_wrappers import PMMChatMessageHistory, PipecatVectorStore
import sys
from unittest.mock import MagicMock
if "langchain_core" in sys.modules and isinstance(sys.modules["langchain_core"], MagicMock):
    del sys.modules["langchain_core"]
if "langchain_core.runnables" in sys.modules and isinstance(sys.modules["langchain_core.runnables"], MagicMock):
    del sys.modules["langchain_core.runnables"]

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

@pytest.fixture
def mock_pmm_memory():
    memory = MagicMock()
    return memory

def test_pmm_chat_message_history_get_messages(mock_pmm_memory):
    # Setup mock events returning from oldest to newest
    mock_events = [
        {"kind": "system_message", "content": "You are a helpful assistant.", "meta": {"session_id": "test_session"}},
        {"kind": "user_message", "content": "Hello", "meta": {"session_id": "test_session"}},
        {"kind": "assistant_message", "content": "Hi there!", "meta": {"session_id": "test_session"}},
        {"kind": "user_message", "content": "Ignore this", "meta": {"session_id": "other_session"}}
    ]
    mock_pmm_memory.get_events_sync.return_value = mock_events

    history = PMMChatMessageHistory(pmm_memory=mock_pmm_memory, session_id="test_session")
    messages = history.messages

    assert len(messages) == 3
    assert isinstance(messages[0], SystemMessage)
    assert messages[0].content == "You are a helpful assistant."

    assert isinstance(messages[1], HumanMessage)
    assert messages[1].content == "Hello"

    assert isinstance(messages[2], AIMessage)
    assert messages[2].content == "Hi there!"

    mock_pmm_memory.get_events_sync.assert_called_once_with(limit=50)

def test_pmm_chat_message_history_add_messages(mock_pmm_memory):
    history = PMMChatMessageHistory(pmm_memory=mock_pmm_memory, session_id="test_session")

    history.add_message(HumanMessage(content="My human message"))
    mock_pmm_memory.add_event_sync.assert_called_with(
        kind="user_message",
        content="My human message",
        meta={"session_id": "test_session"}
    )

    history.add_message(AIMessage(content="My AI response"))
    mock_pmm_memory.add_event_sync.assert_called_with(
        kind="assistant_message",
        content="My AI response",
        meta={"session_id": "test_session"}
    )

@pytest.fixture
def mock_memory_store():
    store = MagicMock()
    store.index.ntotal = 10
    return store

def test_pipecat_vector_store_add_texts(mock_memory_store):
    vector_store = PipecatVectorStore(memory_store=mock_memory_store)

    texts = ["first text", "second text"]
    metadatas = [{"source": "doc1", "summary": "sum1"}, {"source": "doc2"}]

    ids = vector_store.add_texts(texts=texts, metadatas=metadatas)

    assert len(ids) == 2
    assert mock_memory_store.add.call_count == 2
    assert mock_memory_store.add_memory.call_count == 2

    mock_memory_store.add.assert_any_call("first text")
    mock_memory_store.add.assert_any_call("second text")

    # Check that metadatas were passed correctly to add_memory
    mock_memory_store.add_memory.assert_any_call(
        source="doc1",
        raw_text="first text",
        summary="sum1",
        entities=None,
        topics=None
    )

    mock_memory_store.add_memory.assert_any_call(
        source="doc2",
        raw_text="second text",
        summary=None,
        entities=None,
        topics=None
    )

def test_pipecat_vector_store_similarity_search(mock_memory_store):
    mock_memory_store.search.return_value = ["result 1", "result 2"]

    vector_store = PipecatVectorStore(memory_store=mock_memory_store)
    results = vector_store.similarity_search("query text", k=2)

    assert len(results) == 2
    assert results[0].page_content == "result 1"
    assert results[1].page_content == "result 2"

    mock_memory_store.search.assert_called_once_with("query text", k=2)

def test_pipecat_vector_store_from_texts():
    with pytest.raises(NotImplementedError):
        PipecatVectorStore.from_texts(["text"], embedding=None)
