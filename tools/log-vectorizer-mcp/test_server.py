import json
import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock

# Set environment variables BEFORE importing server
os.environ["LOCAL_EMBED_URL"] = "http://fake-url"
os.environ["EMBEDDING_MODEL"] = "fake-model"

# Create a temporary file for the database
temp_db = tempfile.NamedTemporaryFile(delete=False)
os.environ["DATABASE_FILE"] = temp_db.name
temp_db.close()

from server import ingest_log_file, search_logs, cosine_similarity

@pytest.fixture(autouse=True)
def setup_teardown():
    # Clear the database file before each test
    open(os.environ["DATABASE_FILE"], 'w').close()
    yield

def test_cosine_similarity():
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    assert cosine_similarity(v1, v2) == 1.0

    v3 = [0.0, 1.0, 0.0]
    assert cosine_similarity(v1, v3) == 0.0

    # Test orthogonal vectors
    v4 = [1.0, 1.0, 0.0]
    assert abs(cosine_similarity(v1, v4) - 0.7071) < 0.001

    # Test zeros
    assert cosine_similarity([0, 0], [1, 1]) == 0.0

@patch('server.httpx.Client')
@pytest.mark.asyncio
async def test_ingest_log_file(mock_client_class):
    # Setup mock for httpx.Client().post().json()
    mock_instance = mock_client_class.return_value.__enter__.return_value
    mock_response = MagicMock()
    mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
    mock_instance.post.return_value = mock_response

    # Create a mock log file with multi-line stack traces
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as log_file:
        log_file.write("2023-10-25 12:30:45 INFO Starting application\n")
        log_file.write("2023-10-25 12:30:46 ERROR Something went wrong\n")
        log_file.write("Traceback (most recent call last):\n")
        log_file.write("  File \"main.py\", line 10, in <module>\n")
        log_file.write("ValueError: Bad data\n")
        log_file.write("2023-10-25 12:30:47 INFO Shutting down\n")
        log_filepath = log_file.name

    try:
        # Run ingestion
        result = await ingest_log_file(log_filepath)
        assert "Created 3 vectorized text chunks" in result

        # Verify the database contents
        with open(os.environ["DATABASE_FILE"], 'r') as db:
            lines = db.readlines()
            assert len(lines) == 3

            # Chunk 1
            chunk1 = json.loads(lines[0])
            assert chunk1["text"] == "2023-10-25 12:30:45 INFO Starting application"
            assert chunk1["vector"] == [0.1, 0.2, 0.3]

            # Chunk 2 should include the multi-line stack trace
            chunk2 = json.loads(lines[1])
            assert "2023-10-25 12:30:46 ERROR Something went wrong" in chunk2["text"]
            assert "Traceback" in chunk2["text"]
            assert "ValueError: Bad data" in chunk2["text"]

            # Chunk 3
            chunk3 = json.loads(lines[2])
            assert chunk3["text"] == "2023-10-25 12:30:47 INFO Shutting down"
    finally:
        os.remove(log_filepath)

@patch('server.httpx.Client')
@pytest.mark.asyncio
async def test_search_logs(mock_client_class):
    # Setup mock embedding return for the query
    mock_instance = mock_client_class.return_value.__enter__.return_value
    mock_response = MagicMock()
    # Mocking a vector that matches exactly with the second db entry
    mock_response.json.return_value = {"embedding": [1.0, 0.0, 0.0]}
    mock_instance.post.return_value = mock_response

    # Seed the database
    with open(os.environ["DATABASE_FILE"], 'w') as db:
        db.write(json.dumps({"source": "test.log", "text": "Unrelated log", "vector": [0.0, 1.0, 0.0]}) + "\n")
        db.write(json.dumps({"source": "test.log", "text": "Target error message", "vector": [1.0, 0.0, 0.0]}) + "\n")

    # Search for top 1
    result = await search_logs("find error", top_k=1)

    assert "Top 1 relevant log chunks" in result
    assert "Target error message" in result
    assert "Unrelated log" not in result

    # Search for top 2
    result_top2 = await search_logs("find error", top_k=2)
    assert "Target error message" in result_top2
    assert "Unrelated log" in result_top2

@patch('server.httpx.Client')
@pytest.mark.asyncio
async def test_search_logs_no_db(mock_client_class):
    # Setup mock embedding return to avoid httpx hitting real URL during exception test
    mock_instance = mock_client_class.return_value.__enter__.return_value
    mock_response = MagicMock()
    mock_response.json.return_value = {"embedding": [1.0, 0.0, 0.0]}
    mock_instance.post.return_value = mock_response

    # Temporarily remove the DB file to test missing db behavior
    db_path = os.environ["DATABASE_FILE"]
    if os.path.exists(db_path):
        os.remove(db_path)

    result = await search_logs("find error")
    assert "Log database not found" in result
