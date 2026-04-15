import pytest
import asyncio
import sys
from unittest.mock import MagicMock, patch

sys.modules['apscheduler'] = MagicMock()
sys.modules['apscheduler.schedulers'] = MagicMock()
sys.modules['apscheduler.schedulers.asyncio'] = MagicMock()
sys.modules['apscheduler.triggers'] = MagicMock()
sys.modules['apscheduler.triggers.cron'] = MagicMock()
sys.modules['apscheduler.triggers.interval'] = MagicMock()
sys.modules['apscheduler.triggers.date'] = MagicMock()

from pipecatapp.tools.scheduler_tool import SchedulerTool

def test_scheduler_tool_initialization():
    tool = SchedulerTool()
    assert tool.name == "scheduler"
    # tool.scheduler.start should be called
    tool.scheduler.start.assert_called_once()

def test_add_cron_job_invalid():
    tool = SchedulerTool()
    res = asyncio.run(tool.add_cron_job("msg", "invalid cron"))
    assert "Error: Cron expression must have exactly 5 fields" in res

def test_add_cron_job_success():
    tool = SchedulerTool()
    tool.scheduler.add_job.return_value = MagicMock(id="123", next_run_time="now")

    res = asyncio.run(tool.add_cron_job("my cron", "0 9 * * *"))
    assert "Scheduled cron job" in res
    assert "123" in res

def test_add_interval_job_invalid():
    tool = SchedulerTool()
    res = asyncio.run(tool.add_interval_job("msg", 0, 0, 0))
    assert "Error: Interval must be greater than 0" in res

def test_add_interval_job_success():
    tool = SchedulerTool()
    tool.scheduler.add_job.return_value = MagicMock(id="123", next_run_time="now")

    res = asyncio.run(tool.add_interval_job("my interval", minutes=5))
    assert "Scheduled interval job" in res
    assert "123" in res

def test_list_jobs():
    tool = SchedulerTool()

    # Mock empty
    tool.scheduler.get_jobs.return_value = []
    assert "No scheduled jobs" in tool.list_jobs()

    # Mock with job
    mock_job = MagicMock(id="123", next_run_time="now", args=["test msg"])
    tool.scheduler.get_jobs.return_value = [mock_job]
    res = tool.list_jobs()
    assert "test msg" in res
    assert "123" in res

def test_remove_job():
    tool = SchedulerTool()
    res = tool.remove_job("123")
    assert "removed" in res
    tool.scheduler.remove_job.assert_called_with("123")
