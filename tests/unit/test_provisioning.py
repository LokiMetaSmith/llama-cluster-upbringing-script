import unittest
import os
import shutil
import tempfile
import argparse
from unittest.mock import patch, MagicMock
from io import StringIO
import yaml
import sys

# Add scripts directory to path so we can import provisioning
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts')))

import provisioning

class TestProvisioning(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.inventory_file = os.path.join(self.test_dir, "local_inventory.ini")
        with open(self.inventory_file, 'w') as f:
            f.write("[all]\nlocalhost")

        # Patch INVENTORY_FILE in provisioning module
        self.original_inventory = provisioning.INVENTORY_FILE
        provisioning.INVENTORY_FILE = self.inventory_file

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        provisioning.INVENTORY_FILE = self.original_inventory

    def test_load_playbooks_from_manifest(self):
        manifest_path = os.path.join(self.test_dir, "test_manifest.yaml")
        data = [
            {"import_playbook": "playbooks/p1.yaml", "tags": ["t1"]},
            {"import_playbook": "playbooks/p2.yaml"}
        ]
        with open(manifest_path, 'w') as f:
            yaml.dump(data, f)

        playbooks = provisioning.load_playbooks_from_manifest(manifest_path)
        self.assertEqual(len(playbooks), 2)
        self.assertEqual(playbooks[0]['path'], "playbooks/p1.yaml")
        self.assertEqual(playbooks[0]['tags'], ["t1"])
        self.assertEqual(playbooks[1]['tags'], [])

    @patch('provisioning.check_port_open')
    def test_wait_for_ports_freed(self, mock_check):
        # First calls return True (open/busy), then False (closed/free)
        mock_check.side_effect = [True, False]

        with patch('sys.stdout', new=StringIO()) as fake_out:
            provisioning.wait_for_ports_freed([8000], timeout=1)
            output = fake_out.getvalue()
            self.assertIn("Waiting for ports [8000]", output)
            self.assertIn("Port 8000 is free", output)

    @patch('subprocess.run')
    def test_cleanup_memory_for_core_ai(self, mock_run):
        # Mock shutil.which to return True for nomad
        with patch('shutil.which', return_value="/usr/bin/nomad"):
            # Mock job status output
            mock_run.side_effect = [
                MagicMock(stdout="job1\njob2\n"), # nomad job status output
                MagicMock(returncode=0), # stop job1
                MagicMock(returncode=0), # stop job2
                MagicMock(returncode=0)  # free -h
            ]

            provisioning.cleanup_memory_for_core_ai()

            # verify nomad stop calls
            calls = mock_run.call_args_list
            # Check arguments manually as they are complex
            self.assertTrue(any("nomad" in str(c) and "stop" in str(c) for c in calls))

    @patch('subprocess.Popen')
    def test_run_playbook(self, mock_popen):
        # Mock the process object returned by Popen
        mock_process = MagicMock()
        mock_process.stdout = [] # Iterator for stdout
        mock_process.returncode = 0
        mock_process.wait.return_value = None

        mock_popen.return_value = mock_process

        provisioning.run_playbook("test.yaml", {"k": "v"}, "tag1", False)

        args, _ = mock_popen.call_args
        cmd = args[0]
        self.assertEqual(cmd[0], "ansible-playbook")
        self.assertIn("test.yaml", cmd)
        self.assertIn("--extra-vars", cmd)
        self.assertIn("k=v", cmd)
        self.assertIn("--tags", cmd)
        self.assertIn("tag1", cmd)

    @patch('provisioning.purge_nomad_jobs')
    def test_main_purge_jobs(self, mock_purge):
        with patch('argparse.ArgumentParser.parse_known_args') as mock_args:
            # Note: parse_known_args returns (args, unknown)
            mock_args.return_value = (argparse.Namespace(
                role="all", controller_ip=None, tags=None, target_user="u",
                debug=False, continue_run=False, benchmark=False,
                external_model_server=False, leave_services_running=False,
                purge_jobs=True, only_purge=False, deploy_docker=False, run_local=False,
                home_assistant_debug=False, watch=None, verbose=0
            ), [])

            # Mock os.path.exists for manifest
            with patch('os.path.exists', return_value=True):
                 with patch('provisioning.load_playbooks_from_manifest', return_value=[]):
                     provisioning.main()

            mock_purge.assert_called_once()

    @patch('provisioning.purge_nomad_jobs')
    def test_main_only_purge(self, mock_purge):
        with patch('argparse.ArgumentParser.parse_known_args') as mock_args:
             mock_args.return_value = (argparse.Namespace(
                role="all", controller_ip=None, tags=None, target_user="u",
                debug=False, continue_run=False, benchmark=False,
                external_model_server=False, leave_services_running=False,
                purge_jobs=True, only_purge=True, deploy_docker=False, run_local=False,
                home_assistant_debug=False, watch=None, verbose=0
            ), [])

             # We want sys.exit(0) to actually interrupt the flow so main() stops
             with patch('sys.exit') as mock_exit:
                 mock_exit.side_effect = SystemExit(0)

                 with self.assertRaises(SystemExit):
                    provisioning.main()

                 mock_purge.assert_called_once()
                 mock_exit.assert_called_with(0)

if __name__ == '__main__':
    unittest.main()
