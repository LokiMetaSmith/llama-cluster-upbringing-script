import pytest
import os
import json
import base64
from unittest.mock import MagicMock, patch

from cryptography.fernet import Fernet
from pipecatapp.memory import MemoryStore

@pytest.fixture
def temp_store_file(tmp_path):
    return str(tmp_path / "test_memory.json")

@pytest.fixture
def temp_index_file(tmp_path):
    return str(tmp_path / "test_memory.faiss")

@pytest.fixture
def mock_embedding_model():
    mock = MagicMock()
    mock.get_sentence_embedding_dimension.return_value = 128
    mock.encode.return_value = [[0.1] * 128]
    return mock

@pytest.fixture
def mock_faiss_index():
    mock = MagicMock()
    mock.ntotal = 0
    return mock

@patch('pipecatapp.memory.SentenceTransformer')
@patch('pipecatapp.memory.faiss')
def test_unencrypted_memory_store(mock_faiss, mock_st, mock_embedding_model, mock_faiss_index, temp_index_file, temp_store_file, monkeypatch):
    """Test MemoryStore with no encryption key set."""
    monkeypatch.delenv("MEMORY_ENCRYPTION_KEY", raising=False)

    mock_st.return_value = mock_embedding_model
    mock_faiss.IndexFlatL2.return_value = mock_faiss_index
    mock_faiss.read_index.return_value = mock_faiss_index

    store = MemoryStore(index_file=temp_index_file, store_file=temp_store_file)

    assert store.fernet is None

    # Add a memory
    store.add("This is a test memory.")

    assert store.store["0"] == "This is a test memory."

    # Check the actual file contents to ensure it is unencrypted
    with open(temp_store_file, 'r') as f:
        data = json.load(f)
    assert data["0"] == "This is a test memory."

@patch('pipecatapp.memory.SentenceTransformer')
@patch('pipecatapp.memory.faiss')
def test_encrypted_memory_store(mock_faiss, mock_st, mock_embedding_model, mock_faiss_index, temp_index_file, temp_store_file, monkeypatch):
    """Test MemoryStore with encryption key set."""
    key = Fernet.generate_key()
    monkeypatch.setenv("MEMORY_ENCRYPTION_KEY", key.decode())

    mock_st.return_value = mock_embedding_model
    mock_faiss.IndexFlatL2.return_value = mock_faiss_index
    mock_faiss.read_index.return_value = mock_faiss_index

    store = MemoryStore(index_file=temp_index_file, store_file=temp_store_file)

    assert store.fernet is not None

    # Add a memory
    store.add("This is a secret test memory.")

    assert store.store["0"] == "This is a secret test memory."

    # Check the actual file contents to ensure it is encrypted
    with open(temp_store_file, 'r') as f:
        data = json.load(f)

    encrypted_value = data["0"]
    assert encrypted_value != "This is a secret test memory."

    # Verify we can decrypt it
    fernet = Fernet(key)
    decrypted_value = fernet.decrypt(encrypted_value.encode()).decode()
    assert decrypted_value == "This is a secret test memory."

@patch('pipecatapp.memory.SentenceTransformer')
@patch('pipecatapp.memory.faiss')
def test_encrypted_store_loads_legacy_unencrypted_data(mock_faiss, mock_st, mock_embedding_model, mock_faiss_index, temp_index_file, temp_store_file, monkeypatch):
    """Test MemoryStore gracefully handles plain text data when encryption is enabled."""
    key = Fernet.generate_key()
    monkeypatch.setenv("MEMORY_ENCRYPTION_KEY", key.decode())

    mock_st.return_value = mock_embedding_model
    mock_faiss.IndexFlatL2.return_value = mock_faiss_index
    mock_faiss.read_index.return_value = mock_faiss_index

    # Write some unencrypted legacy data to the store file
    legacy_data = {"0": "Legacy plaintext memory."}
    with open(temp_store_file, 'w') as f:
        json.dump(legacy_data, f)

    store = MemoryStore(index_file=temp_index_file, store_file=temp_store_file)

    # Verify legacy data loaded successfully
    assert "0" in store.store
    assert store.store["0"] == "Legacy plaintext memory."

    # Mock index so the next ID is 1 to preserve legacy data at '0'
    mock_faiss_index.ntotal = 1

    # Adding a new memory should encrypt both legacy and new data on next save
    store.add("New memory.")

    with open(temp_store_file, 'r') as f:
        saved_data = json.load(f)

    fernet = Fernet(key)
    assert fernet.decrypt(saved_data["0"].encode()).decode() == "Legacy plaintext memory."
    assert fernet.decrypt(saved_data["1"].encode()).decode() == "New memory."

@patch('pipecatapp.memory.SentenceTransformer')
@patch('pipecatapp.memory.faiss')
def test_unencrypted_store_loads_encrypted_data_as_is(mock_faiss, mock_st, mock_embedding_model, mock_faiss_index, temp_index_file, temp_store_file, monkeypatch):
    """Test MemoryStore handles encrypted data as string if encryption key is removed."""
    monkeypatch.delenv("MEMORY_ENCRYPTION_KEY", raising=False)

    mock_st.return_value = mock_embedding_model
    mock_faiss.IndexFlatL2.return_value = mock_faiss_index
    mock_faiss.read_index.return_value = mock_faiss_index

    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_memory = fernet.encrypt(b"This data is encrypted.").decode()

    # Write encrypted data directly to store
    encrypted_data = {"0": encrypted_memory}
    with open(temp_store_file, 'w') as f:
        json.dump(encrypted_data, f)

    store = MemoryStore(index_file=temp_index_file, store_file=temp_store_file)

    # Verify it loaded the raw encrypted string since it doesn't have the key to decrypt
    assert "0" in store.store
    assert store.store["0"] == encrypted_memory
