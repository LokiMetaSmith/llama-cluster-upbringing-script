import pytest
import asyncio
from pipecatapp.tools.frugal_sandbox_tool import FrugalSandboxTool

@pytest.mark.asyncio
async def test_frugal_sandbox_success_high_value():
    """Test standard successful execution of code with high value contribution and no escalation."""
    tool = FrugalSandboxTool()

    task_query = "Print out the first 5 prime numbers to verify the generator"
    proposed_code = "print('Prime numbers: 2, 3, 5, 7, 11')"

    report = await tool.run(
        task_query=task_query,
        proposed_code=proposed_code,
        expected_output_pattern=r"2,\s*3,\s*5"
    )

    # Basic validations
    assert report is not None
    assert "execution_metrics" in report
    assert "evaluation_scores" in report
    assert "escalation_decision" in report

    metrics = report["execution_metrics"]
    scores = report["evaluation_scores"]
    decision = report["escalation_decision"]

    assert metrics["exit_code"] == 0
    assert metrics["timed_out"] is False
    assert metrics["duration_ms"] > 0
    assert metrics["peak_rss_mb"] > 0

    assert scores["execution_cost_score"] >= 0
    assert scores["value_contribution_score"] >= 4.0  # Success threshold
    assert scores["value_density_ratio"] >= 0.1

    assert decision["escalation_recommended"] is False
    assert "Low-cost success" in decision["recommendation"]
    assert "2, 3, 5, 7, 11" in report["stdout"]

@pytest.mark.asyncio
async def test_frugal_sandbox_syntax_error_escalation():
    """Test that a syntax error in the code results in low value contribution and recommends escalation."""
    tool = FrugalSandboxTool()

    task_query = "Calculate factorial of 5"
    proposed_code = "print(factorial(5)"  # SyntaxError: missing closing parenthesis

    report = await tool.run(
        task_query=task_query,
        proposed_code=proposed_code
    )

    metrics = report["execution_metrics"]
    scores = report["evaluation_scores"]
    decision = report["escalation_decision"]

    assert metrics["exit_code"] != 0
    assert scores["value_contribution_score"] == 0.0
    assert scores["value_density_ratio"] == 0.0
    assert decision["escalation_recommended"] is True
    assert "Escalate to frontier model: code execution failed" in decision["recommendation"]

@pytest.mark.asyncio
async def test_frugal_sandbox_empty_output_escalation():
    """Test that code producing empty stdout leads to low value and recommends escalation."""
    tool = FrugalSandboxTool()

    task_query = "Get active user count"
    proposed_code = "pass"

    report = await tool.run(
        task_query=task_query,
        proposed_code=proposed_code
    )

    metrics = report["execution_metrics"]
    scores = report["evaluation_scores"]
    decision = report["escalation_decision"]

    assert metrics["exit_code"] == 0
    assert scores["value_contribution_score"] == 1.0  # Empty output base
    assert decision["escalation_recommended"] is True
    assert "insufficient output value/contribution" in decision["recommendation"]

@pytest.mark.asyncio
async def test_frugal_sandbox_pattern_mismatch_escalation():
    """Test that failed expected pattern match impacts the scores and escalation decision if value is low."""
    tool = FrugalSandboxTool()

    task_query = "Compute user average age"
    proposed_code = "print('Done')"

    # Pattern expects 'average age' or a float
    report = await tool.run(
        task_query=task_query,
        proposed_code=proposed_code,
        expected_output_pattern=r"average age:\s*\d+"
    )

    metrics = report["execution_metrics"]
    scores = report["evaluation_scores"]
    decision = report["escalation_decision"]

    assert metrics["exit_code"] == 0
    # No pattern match and minimal keyword overlap, should have lower value_contribution
    assert scores["value_contribution_score"] < 4.0
    assert decision["escalation_recommended"] is True
    assert "insufficient output value/contribution" in decision["recommendation"]

@pytest.mark.asyncio
async def test_frugal_sandbox_timeout_escalation():
    """Test that an execution timeout is caught and escalates."""
    tool = FrugalSandboxTool()

    task_query = "Wait for thread job to finish"
    proposed_code = "import time\ntime.sleep(5)"

    report = await tool.run(
        task_query=task_query,
        proposed_code=proposed_code,
        timeout_seconds=1
    )

    metrics = report["execution_metrics"]
    scores = report["evaluation_scores"]
    decision = report["escalation_decision"]

    assert metrics["timed_out"] is True
    assert metrics["exit_code"] == 124
    assert scores["value_contribution_score"] == 0.0
    assert decision["escalation_recommended"] is True
    assert "timed out" in decision["recommendation"]
