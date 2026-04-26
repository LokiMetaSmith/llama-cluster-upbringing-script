import unittest
import os
import tempfile
import asyncio
import shutil
from unittest.mock import MagicMock, AsyncMock, patch

# Add project root to sys.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp')))

import sys
sys.modules['numpy'] = MagicMock()
sys.modules['services.gemma_e2b_service'] = MagicMock()

class MockObserver:
    def __init__(self): pass
    def schedule(self, *args, **kwargs): pass
    def start(self): pass
    def stop(self): pass
    def join(self): pass

class MockFileSystemEventHandler:
    pass

mock_watchdog = MagicMock()
mock_watchdog.observers.Observer = MockObserver
mock_watchdog.events.FileSystemEventHandler = MockFileSystemEventHandler
sys.modules['watchdog'] = mock_watchdog
sys.modules['watchdog.observers'] = mock_watchdog.observers
sys.modules['watchdog.events'] = mock_watchdog.events

from services.obsidian_gardener import ObsidianGardener

class TestObsidianGardener(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

        self.mock_runner_instance = MagicMock()
        self.mock_runner_instance.run = AsyncMock(return_value={"status": "success", "data": "test_output"})

        self.mock_runner_class = MagicMock(return_value=self.mock_runner_instance)

        self.gardener = ObsidianGardener(vault_path=self.temp_dir, workflow_runner_class=self.mock_runner_class)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    async def test_process_markdown_no_agent_tag(self):
        file_path = os.path.join(self.temp_dir, "test1.md")
        with open(file_path, "w") as f:
            f.write("Just some regular text. <!-- run: workflow.yaml -->")

        await self.gardener._process_markdown(file_path)

        self.mock_runner_class.assert_not_called()

    async def test_process_markdown_with_directive(self):
        file_path = os.path.join(self.temp_dir, "test2.md")
        with open(file_path, "w") as f:
            f.write("#agent\nHere is a task. <!-- run: workflow.yaml -->")

        # Create dummy workflow file to pass os.path.exists check
        workflow_path = os.path.join(self.temp_dir, "workflow.yaml")
        with open(workflow_path, "w") as f:
            f.write("dummy workflow")

        await self.gardener._process_markdown(file_path)

        self.mock_runner_class.assert_called_once()
        self.mock_runner_instance.run.assert_called_once()

        # Check if result was appended
        with open(file_path, "r") as f:
            content = f.read()

        self.assertIn("<!-- done: workflow.yaml -->", content)
        self.assertIn("test_output", content)

    async def test_process_markdown_already_processed(self):
        file_path = os.path.join(self.temp_dir, "test3.md")
        with open(file_path, "w") as f:
            f.write("#agent\nHere is a task. <!-- run: workflow.yaml -->\n<!-- done: workflow.yaml -->")

        await self.gardener._process_markdown(file_path)

        self.mock_runner_class.assert_not_called()

if __name__ == '__main__':
    unittest.main()
