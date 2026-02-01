import os
import shutil
import sqlite3
import pytest
from pipecatapp.workflow.history import WorkflowHistory

@pytest.fixture
def temp_db_path():
    path = os.path.abspath("/tmp/test_workflow_history_pytest.db")
    yield path
    # Teardown: Remove file and clear cache

    # Critical: Close connection and clear the global cache to ensure isolation
    if hasattr(WorkflowHistory, '_instances') and path in WorkflowHistory._instances:
        # Close the connection explicitly
        instance = WorkflowHistory._instances[path]
        # Only call close if it exists (which it should now)
        if hasattr(instance, 'close'):
            instance.close()
        del WorkflowHistory._instances[path]

    if os.path.exists(path):
        os.remove(path)
    dir_path = os.path.dirname(path)
    if os.path.exists(dir_path) and dir_path != "/tmp":
        shutil.rmtree(dir_path)

def test_workflow_history_init(temp_db_path):
    history = WorkflowHistory(db_path=temp_db_path)
    assert os.path.exists(temp_db_path)

    # Check that we can access the DB manually
    # Note: With WAL mode, there might be .shm and .wal files.
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workflow_runs'")
    assert cursor.fetchone() is not None
    conn.close()

def test_workflow_history_singleton_init(temp_db_path, mocker):
    # First init should call _init_db
    history1 = WorkflowHistory(db_path=temp_db_path)

    assert temp_db_path in WorkflowHistory._instances
    assert history1 is WorkflowHistory._instances[temp_db_path]

    # Mock os.makedirs to ensure it's not called again
    mock_makedirs = mocker.patch('os.makedirs')

    # Second init should return the same instance and NOT run _init_db
    history2 = WorkflowHistory(db_path=temp_db_path)

    # Assert identity
    assert history1 is history2

    # Assert os.makedirs was NOT called
    assert not mock_makedirs.called

    # Assert connection is the same
    assert history1.conn is history2.conn
