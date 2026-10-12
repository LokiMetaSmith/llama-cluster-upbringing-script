import json
import httpx
from typing import Dict, Any, List


class ReverseEngineerTool:
    def __init__(self):
        self.tool_server_url = "http://tool-server-rea.service.consul:8000"

    def get_component_spec(self) -> Dict[str, Any]:
        return {
            "name": "reverse_engineer_tool",
            "description": "Analyzes and reverse engineers native binaries, javascript applications, or websites using the REA MCP server.",
            "inputs": [
                {
                    "name": "target_path",
                    "type": "String",
                    "description": "The local filesystem path to the application, binary, or script to analyze.",
                },
                {
                    "name": "tool_name",
                    "type": "String",
                    "description": "The REA sub-tool to invoke (e.g. 'analyze-javascript-application', 'analyze-native-binary').",
                },
            ],
            "outputs": [
                {
                    "name": "analysis_result",
                    "type": "String",
                    "description": "JSON string containing the analysis results, decompiled code, or AST information.",
                }
            ],
        }

    def execute(self, target_path: str, tool_name: str) -> str:
        try:
            with httpx.Client(timeout=120.0) as client:
                response = client.post(
                    f"{self.tool_server_url}/run_tool/{tool_name}",
                    json={"target_path": target_path},
                )
                response.raise_for_status()
                return json.dumps(response.json(), indent=2)
        except Exception as e:
            return json.dumps(
                {"error": f"Reverse engineering analysis failed: {str(e)}"}
            )
