import os
import json
import tempfile
import pytest
from unittest.mock import patch

from server import ingest_log_file

@pytest.mark.asyncio
@patch("server.get_local_embedding")
async def test_ingest_log_file(mock_get_local_embedding):
    # Mock the embedding generation to return a fixed vector
    mock_get_local_embedding.return_value = [0.1, 0.2, 0.3]

    # Create a temporary log file with timestamped entries and stack traces
    log_content = """2023-10-25 12:30:45 INFO Starting server...
2023-10-25 12:30:46 WARN High memory usage detected.
2023-10-25 12:30:47 ERROR Unhandled exception in worker thread:
Traceback (most recent call last):
  File "worker.py", line 42, in process
    1 / 0
ZeroDivisionError: division by zero
2023-10-25 12:30:48 INFO Server recovering.
"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_log_file:
        temp_log_file.write(log_content)
        temp_log_filepath = temp_log_file.name

    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_db_file:
        temp_db_filepath = temp_db_file.name

    try:
        # Patch the DATABASE_FILE globally in the server module
        with patch("server.DATABASE_FILE", temp_db_filepath):
            # Run the tool
            result = await ingest_log_file(temp_log_filepath)

            # Check the tool result output string
            assert "Successfully ingested" in result
            assert "Created 4 vectorized text chunks" in result

            # Verify the database was created and contains the correct entries
            with open(temp_db_filepath, 'r', encoding='utf-8') as db:
                lines = db.readlines()
                assert len(lines) == 4

                # Check the first entry
                entry1 = json.loads(lines[0])
                assert entry1["source"] == temp_log_filepath
                assert "Starting server..." in entry1["text"]
                assert entry1["vector"] == [0.1, 0.2, 0.3]

                # Check the third entry (which includes the multi-line stack trace)
                entry3 = json.loads(lines[2])
                assert "Unhandled exception" in entry3["text"]
                assert "Traceback" in entry3["text"]
                assert "ZeroDivisionError: division by zero" in entry3["text"]
                # Ensure the multi-line is kept together
                assert "\n" in entry3["text"]

    finally:
        # Clean up temporary files
        os.remove(temp_log_filepath)
        os.remove(temp_db_filepath)
