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
    if os.path.exists(path):
        os.remove(path)
    dir_path = os.path.dirname(path)
    if os.path.exists(dir_path) and dir_path != "/tmp":
        shutil.rmtree(dir_path)

    # Critical: Clear the global cache to ensure isolation
    if path in WorkflowHistory._initialized_paths:
        WorkflowHistory._initialized_paths.remove(path)

def test_workflow_history_init(temp_db_path):
    history = WorkflowHistory(db_path=temp_db_path)
    assert os.path.exists(temp_db_path)

    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workflow_runs'")
    assert cursor.fetchone() is not None
    conn.close()

def test_workflow_history_singleton_init(temp_db_path, mocker):
    # First init should call _init_db
    history1 = WorkflowHistory(db_path=temp_db_path)

    assert temp_db_path in WorkflowHistory._initialized_paths

    # Second init should be fast and not call os.makedirs/sqlite connect for table creation
    # We mock os.makedirs to ensure it's not called again

    mock_makedirs = mocker.patch('os.makedirs')
    # Note: We can't easily mock sqlite3.connect here without potentially affecting other things
    # unless we're very careful, but verifying os.makedirs is a strong enough signal
    # since _init_db calls it first.

    history2 = WorkflowHistory(db_path=temp_db_path)

    # Assert os.makedirs was NOT called because we hit the cache
    assert not mock_makedirs.called
