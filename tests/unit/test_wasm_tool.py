import unittest
from unittest.mock import patch, MagicMock
import os
import json
from pipecatapp.tools.wasm_tool import WasmTool

class TestWasmTool(unittest.TestCase):

    @patch('os.path.exists')
    @patch('extism.Plugin')
    def test_process_text_success(self, mock_plugin_class, mock_exists):
        # Setup mocks
        mock_exists.return_value = True
        mock_plugin = MagicMock()
        mock_plugin_class.return_value = mock_plugin

        # Simulate WASM returning reversed string in json bytes format
        mock_plugin.call.return_value = b'{"result": "!dlroW olleH"}'

        tool = WasmTool(wasm_path="/dummy/path.wasm")
        result = tool.process_text("reverse", "Hello World!")

        self.assertEqual(result, "!dlroW olleH")

        # Verify call arguments
        mock_plugin.call.assert_called_once()
        args, _ = mock_plugin.call.call_args
        self.assertEqual(args[0], "process_text")
        parsed_input = json.loads(args[1])
        self.assertEqual(parsed_input["action"], "reverse")
        self.assertEqual(parsed_input["text"], "Hello World!")

    @patch('os.path.exists')
    def test_process_text_missing_file(self, mock_exists):
        mock_exists.return_value = False

        tool = WasmTool(wasm_path="/missing.wasm")
        result = tool.process_text("reverse", "text")

        self.assertIn("Error: WASM module not found", result)

    @patch('os.path.exists')
    @patch('extism.Plugin')
    def test_execute_custom_success(self, mock_plugin_class, mock_exists):
        mock_exists.return_value = True
        mock_plugin = MagicMock()
        mock_plugin_class.return_value = mock_plugin
        mock_plugin.call.return_value = b'{"status": "success", "value": 42}'

        tool = WasmTool(wasm_path="/dummy/path.wasm")
        result = tool.execute_custom("compute_magic", {"input": 10})

        # Should return stringified dict
        self.assertIn("success", result)
        self.assertIn("42", result)

        mock_plugin.call.assert_called_once_with("compute_magic", '{"input": 10}')

if __name__ == '__main__':
    unittest.main()
