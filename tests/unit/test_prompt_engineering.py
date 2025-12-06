import os
import sys
import json
import pytest
import shutil
import tempfile
from unittest.mock import MagicMock, patch, mock_open, AsyncMock

# Ensure the prompt_engineering directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../prompt_engineering')))

import evolve
import run_campaign
import promote_agent
import visualize_archive

class TestEvolve:
    @pytest.fixture
    def mock_archive(self, tmp_path):
        archive_dir = tmp_path / "archive"
        archive_dir.mkdir()
        return archive_dir

    def test_select_parent_from_archive_empty(self, mock_archive):
        with patch("evolve.os.path.dirname", return_value=str(mock_archive.parent)):
            with patch("evolve.glob.glob", return_value=[]):
                path, agent_id = evolve.select_parent_from_archive()
                assert agent_id is None
                assert "app.py" in path

    def test_select_parent_from_archive_populated(self, mock_archive):
        # Create a dummy agent and metadata
        agent_id = "test_agent"
        meta_file = mock_archive / f"{agent_id}.json"
        with open(meta_file, "w") as f:
            json.dump({"fitness": 0.9}, f)

        agent_file = mock_archive / f"{agent_id}.py"
        with open(agent_file, "w") as f:
            f.write("# dummy code")

        with patch("evolve.os.path.dirname", return_value=str(mock_archive.parent)):
             with patch("evolve.glob.glob", return_value=[str(meta_file)]):
                 path, selected_id = evolve.select_parent_from_archive()
                 assert selected_id == agent_id
                 assert path == str(agent_file)

    @pytest.mark.asyncio
    async def test_run_evolution(self, mock_archive):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("evolve.select_parent_from_archive", return_value=("dummy_path.py", "parent_id")):
                with patch("evolve.os.path.exists", return_value=True):
                    # Mock the AsyncMock for the run method
                    mock_run_result = MagicMock(metrics={"fitness": 1.0})
                    mock_openevolve = MagicMock()
                    mock_openevolve.run = AsyncMock(return_value=mock_run_result)

                    with patch("evolve.OpenEvolve", return_value=mock_openevolve):
                        # We need to verify os.environ *during* execution, not after
                        # because run_evolution cleans up env vars in finally block
                        with patch("evolve.OpenEvolve.run", new_callable=AsyncMock) as mock_run:
                            mock_run.return_value = mock_run_result

                            # We can check if env var was set by inspecting what happened inside
                            # But since run_evolution instantiates OpenEvolve, we need to be careful.
                            # The simplest way is to check if it was set before cleanup.
                            # We can mock the finally block or check inside the mocked run?
                            # Let's check inside the mocked run.

                            async def side_effect(*args, **kwargs):
                                assert os.environ["PARENT_AGENT_ID"] == "parent_id"
                                return mock_run_result

                            mock_openevolve.run.side_effect = side_effect

                            await evolve.run_evolution()

                            mock_openevolve.run.assert_called_once()

class TestRunCampaign:
    def test_run_campaign(self):
        generations = 3
        with patch("subprocess.Popen") as mock_popen:
            # Mock the process output and wait
            process_mock = MagicMock()
            process_mock.stdout = ["Generation output line 1\n", "Generation output line 2\n"]
            process_mock.wait.return_value = None
            process_mock.returncode = 0
            mock_popen.return_value = process_mock

            with patch("os.path.exists", return_value=True):
                run_campaign.run_campaign(generations)

            assert mock_popen.call_count == generations

    def test_analyze_archive(self, tmp_path):
        archive_dir = tmp_path / "archive"
        archive_dir.mkdir()

        # Create dummy agents
        for i in range(3):
            meta = {"fitness": 0.1 * i, "id": f"agent_{i}", "rationale": "test"}
            with open(archive_dir / f"agent_{i}.json", "w") as f:
                json.dump(meta, f)

        with patch("run_campaign.glob.glob", return_value=[str(p) for p in archive_dir.glob("*.json")]):
             with patch("run_campaign._generate_report") as mock_report:
                 run_campaign.analyze_archive()
                 mock_report.assert_called_once()
                 args, _ = mock_report.call_args
                 assert len(args[0]) == 3 # Should contain all 3 agents (since we take top 5)

class TestPromoteAgent:
    @pytest.fixture
    def mock_paths(self, tmp_path):
        base_dir = tmp_path
        archive_dir = base_dir / "archive"
        archive_dir.mkdir()

        # Target app path
        target_dir = base_dir / "ansible/roles/pipecatapp/files"
        target_dir.mkdir(parents=True)
        target_app = target_dir / "app.py"
        target_app.touch()

        return base_dir, archive_dir, target_app

    def test_promote_agent_manual(self, mock_paths):
        base_dir, archive_dir, target_app = mock_paths
        agent_id = "manual_agent"
        agent_file = archive_dir / f"{agent_id}.py"
        agent_file.write_text("# new code")

        with patch("promote_agent.os.path.dirname", return_value=str(base_dir)):
            with patch("promote_agent.os.path.abspath", return_value=str(target_app)): # Fix target path resolution
                 promote_agent.promote_agent(agent_id, is_best=False)

                 # Verify file copy
                 assert target_app.read_text() == "# new code"
                 assert (target_app.parent / "app.py.bak").exists()

    def test_find_best_agent(self, mock_paths):
        base_dir, archive_dir, _ = mock_paths

        # Create agents
        with open(archive_dir / "a1.json", "w") as f: json.dump({"fitness": 0.5}, f)
        with open(archive_dir / "a2.json", "w") as f: json.dump({"fitness": 0.9}, f)

        with patch("promote_agent.glob.glob", return_value=[str(p) for p in archive_dir.glob("*.json")]):
             # Patch dirname to point to our mock base_dir's parent because find_best_agent constructs path relative to __file__
             with patch("promote_agent.os.path.dirname", return_value=str(base_dir)):
                 agent_id, fitness = promote_agent.find_best_agent()
                 assert agent_id == "a2"
                 assert fitness == 0.9

class TestVisualizeArchive:
    def test_visualize_archive(self, tmp_path):
        archive_dir = tmp_path / "archive"
        archive_dir.mkdir()

        with patch("visualize_archive.os.path.dirname", return_value=str(tmp_path)):
            with patch("visualize_archive.glob.glob", return_value=[]): # Empty archive
                visualize_archive.visualize_archive()
                # Should just return without error

            # With mock graphviz
            with patch("visualize_archive.glob.glob", return_value=["dummy.json"]):
                 with patch("builtins.open", mock_open(read_data='{"fitness": 0.5, "parent": "root"}')):
                     mock_dot = MagicMock()
                     with patch("visualize_archive.Digraph", return_value=mock_dot):
                         visualize_archive.visualize_archive()
                         mock_dot.render.assert_called_once()
