import pytest
import os
import json
import sqlite3
from tools.goal_tool import GoalTool

@pytest.fixture
def temp_db_path(tmp_path):
    return str(tmp_path / "test_goals.db")

@pytest.fixture
def goal_tool(temp_db_path):
    tool = GoalTool(db_path=temp_db_path)
    yield tool
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)

def test_create_and_get_goal(goal_tool):
    task_id = "task-123"
    objective = "Solve the KIRO network optimization problem."

    # Initial state should be empty
    assert goal_tool.get_goal(task_id) == "No active goal found for this task."

    # Create goal
    result = goal_tool.create_goal(task_id, objective)
    assert "Successfully created" in result

    # Get goal
    goal_json = goal_tool.get_goal(task_id)
    assert goal_json != "No active goal found for this task."

    goal = json.loads(goal_json)
    assert goal["task_id"] == task_id
    assert goal["objective"] == objective
    assert goal["status"] == "active"

def test_update_goal(goal_tool):
    task_id = "task-456"
    goal_tool.create_goal(task_id, "Temporary objective")

    result = goal_tool.update_goal(task_id, "completed")
    assert "Successfully updated" in result

    # Should no longer be active
    assert goal_tool.get_goal(task_id) == "No active goal found for this task."

def test_schedule_wakeup(goal_tool, temp_db_path):
    task_id = "task-789"
    result = goal_tool.schedule_wakeup(task_id, 300, "Waiting for deployment")
    assert "Wakeup scheduled" in result

    # Verify in DB directly since schedule_wakeup doesn't have a direct reader method
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, context FROM wakeups WHERE task_id = ?", (task_id,))
    row = cursor.fetchone()
    assert row[0] == task_id
    assert row[1] == "Waiting for deployment"
    conn.close()
