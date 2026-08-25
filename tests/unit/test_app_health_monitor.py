import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from pipecatapp.services.app_health_monitor import AppHealthMonitor

@pytest.mark.asyncio
async def test_app_health_monitor_reconcile_trigger():
    monitor = AppHealthMonitor(interval=10)

    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = [
        {"ID": "pihole", "Status": "dead"}
    ]

    with patch("httpx.AsyncClient.get", return_value=mock_res):
        with patch.object(monitor, "trigger_reconciliation", new_callable=AsyncMock) as mock_trigger:
            await monitor.check_and_reconcile()
            mock_trigger.assert_called_once_with("pihole")

@pytest.mark.asyncio
async def test_app_health_monitor_trigger_reconciliation_exec():
    monitor = AppHealthMonitor(interval=10)

    mock_proc = AsyncMock()
    mock_proc.returncode = 0
    mock_proc.communicate.return_value = (b"", b"")

    with patch("asyncio.create_subprocess_exec", return_value=mock_proc) as mock_subproc:
        await monitor.trigger_reconciliation("pihole")
        mock_subproc.assert_called_once()
        args = mock_subproc.call_args[0]
        assert "playbooks/deploy_community_app.yaml" in args
        assert "app_name=pihole" in args[7]
