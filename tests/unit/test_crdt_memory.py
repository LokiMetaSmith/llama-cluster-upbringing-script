import pytest
from pipecatapp.memory_backends_impl.crdt_backend import CRDTMemoryBackend
from pipecatapp.memory import Document

def test_crdt_memory_backend_add_and_query():
    backend = CRDTMemoryBackend(node_id="node-1")
    backend.add("The secret code is 12345")

    results = backend.query("secret code")
    assert len(results) == 1
    assert results[0] == "The secret code is 12345"

def test_crdt_memory_backend_merge():
    backend1 = CRDTMemoryBackend(node_id="node-1")
    backend2 = CRDTMemoryBackend(node_id="node-2")

    backend1.add("Message from node 1")
    backend2.add("Message from node 2")

    state1 = backend1.get_state()
    backend2.merge(state1)

    results = backend2.query("node 1")
    assert len(results) == 1
    assert results[0] == "Message from node 1"

    # Both should be in backend 2 now
    all_docs = backend2.filter_documents()
    assert len(all_docs) == 2

def test_crdt_memory_backend_write_document():
    backend = CRDTMemoryBackend(node_id="node-1")
    doc = Document(id="test-1", content="Hello", metadata={"test": True})
    backend.write_documents([doc])

    docs = backend.filter_documents()
    assert len(docs) == 1
    assert docs[0].content == "Hello"
    assert docs[0].metadata["test"] is True
def test_crdt_memory_backend_delete_skill():
    backend = CRDTMemoryBackend(node_id="node-1")
    backend.save_skill("test_skill", "A test skill", "Do this and that")

    assert backend.get_skill("test_skill") is not None
    assert backend.delete_skill("test_skill") is True
    assert backend.get_skill("test_skill") is None

    # Check that deleted skills stay deleted after merge (tombstones work)
    backend2 = CRDTMemoryBackend(node_id="node-2")
    # Simulate an old state merging
    old_state = {"added": list(backend.doc.added), "removed": []}
    backend.merge(old_state)
    # Because it is an ORSet, the remove should have added a tombstone, so it shouldn't reappear
    assert backend.get_skill("test_skill") is None
