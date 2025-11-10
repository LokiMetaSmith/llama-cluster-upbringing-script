import unittest
import os
import json
from unittest.mock import patch, mock_open

# Add the reflection directory to the Python path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'reflection')))

class TestAdaptationManager(unittest.TestCase):

    def test_import(self):
        """Ensure the adaptation_manager script can be imported without errors."""
        try:
            import adaptation_manager
        except ImportError as e:
            self.fail(f"Failed to import adaptation_manager: {e}")

    @patch("builtins.open", new_callable=mock_open, read_data='{"job_id": "test_job"}')
    @patch("subprocess.Popen")
    def test_main_flow(self, mock_popen, mock_file):
        """Test the main execution flow of the adaptation_manager."""
        from adaptation_manager import main

        # Mock the command-line arguments
        with patch.object(sys, 'argv', ['adaptation_manager.py', 'dummy_diagnostics.json']):
            main()

        # Verify that the test case file was written
        # We iterate through the calls to find the one that writes the test case
        written_filepath = None
        for call in mock_file.call_args_list:
            # call is a tuple of (args, kwargs)
            filepath = call[0][0]
            mode = call[0][1]
            if mode == 'w' and 'failure_test_job_' in os.path.basename(filepath):
                self.assertIn('prompt_engineering/generated_evaluators', filepath)
                written_filepath = filepath
                break

        self.assertIsNotNone(written_filepath, "Did not find the call to write the test case file.")

        # Verify that the evolution script was called with the correct path
        mock_popen.assert_called_once()
        args, _ = mock_popen.call_args
        self.assertIn("evolve.py", args[0][1])
        self.assertIn("--test-case", args[0])
        self.assertEqual(args[0][-1], written_filepath)

if __name__ == '__main__':
    unittest.main()
