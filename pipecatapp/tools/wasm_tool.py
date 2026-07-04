import extism
import json
import os
import logging
from typing import Optional, Dict, Any

class WasmTool:
    """A tool to execute lightweight WASM plugins using Extism."""

    def __init__(self, wasm_path: Optional[str] = None):
        self.name = "wasm_tool"

        # Default to the text processor if no path is provided
        if wasm_path is None:
            # We assume the poc is compiled and present, otherwise this tool requires a valid path.
            # In a real deployment, the wasm module should be copied to a permanent location.
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
            self.wasm_path = os.path.join(project_root, "poc/wasm_tool_bridge/text_processor/target/wasm32-wasip1/release/text_processor.wasm")
        else:
            self.wasm_path = wasm_path

    def process_text(self, action: str, text: str) -> str:
        """
        Processes text using a WASM plugin.

        Args:
            action (str): The action to perform (e.g., 'uppercase', 'lowercase', 'reverse').
            text (str): The text to process.
        """
        if not os.path.exists(self.wasm_path):
            return f"Error: WASM module not found at {self.wasm_path}. Please ensure it is compiled."

        try:
            manifest = {"wasm": [{"path": self.wasm_path}]}
            plugin = extism.Plugin(manifest, wasi=True)

            input_data = json.dumps({
                "action": action,
                "text": text
            })

            result = plugin.call("process_text", input_data)

            # The extism call returns bytes, we decode it and load as json
            if isinstance(result, bytes):
                result_str = result.decode('utf-8')
            else:
                result_str = result

            parsed_result = json.loads(result_str)
            return parsed_result.get("result", str(parsed_result))

        except Exception as e:
            logging.error(f"Failed to execute WASM plugin: {e}")
            return f"Error executing WASM plugin: {e}"

    def execute_custom(self, function_name: str, input_payload: Dict[str, Any]) -> str:
        """
        Executes a custom function on the WASM plugin.

        Args:
            function_name (str): The name of the exported WASM function to call.
            input_payload (dict): The input data to pass to the function as JSON.
        """
        if not os.path.exists(self.wasm_path):
            return f"Error: WASM module not found at {self.wasm_path}."

        try:
            manifest = {"wasm": [{"path": self.wasm_path}]}
            plugin = extism.Plugin(manifest, wasi=True)

            input_data = json.dumps(input_payload)
            result = plugin.call(function_name, input_data)

            if isinstance(result, bytes):
                result_str = result.decode('utf-8')
            else:
                result_str = result

            try:
                parsed_result = json.loads(result_str)
                return str(parsed_result)
            except json.JSONDecodeError:
                return result_str

        except Exception as e:
            logging.error(f"Failed to execute custom WASM function '{function_name}': {e}")
            return f"Error executing custom WASM function '{function_name}': {e}"
