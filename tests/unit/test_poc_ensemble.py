import unittest
import asyncio
import os
import sys
from unittest.mock import MagicMock, AsyncMock, patch
import logging

# Add the ansible/roles/pipecatapp/files directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible/roles/pipecatapp/files')))

from workflow.runner import WorkflowRunner
from workflow.context import WorkflowContext
# Ensure nodes are registered
from workflow.nodes import base_nodes, llm_nodes

# Mock external experts config
MOCK_EXPERTS_CONFIG = {
    "openai_gpt4": {
        "base_url": "https://api.openai.com/v1",
        "api_key_env": "OPENAI_API_KEY",
        "model": "gpt-4-turbo"
    },
    "openrouter_gpt5": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "OPENROUTER_API_KEY",
        "model": "openai/gpt-5"
    },
    "openrouter_claude_sonnet": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "OPENROUTER_API_KEY",
        "model": "anthropic/claude-3.5-sonnet"
    },
    "openrouter_gemini_flash": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "OPENROUTER_API_KEY",
        "model": "google/gemini-2.0-flash-001"
    }
}

class TestPoCEnsemble(unittest.TestCase):
    def setUp(self):
        # Set dummy env vars for keys
        os.environ["OPENAI_API_KEY"] = "sk-dummy"
        os.environ["OPENROUTER_API_KEY"] = "sk-or-dummy"
        self.workflow_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible/roles/pipecatapp/files/workflows/poc_ensemble.yaml'))

    @patch('httpx.AsyncClient')
    def test_workflow_execution(self, mock_client_cls):
        # Setup Mock Client
        mock_client = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        # Configure responses for each node call
        # We expect calls for Orchestrator, Architect, Librarian, Designer, Synthesizer (internal logic or mock)
        # Note: Synthesizer uses SimpleLLMNode which tries to hit Consul. We should mock that too or ensure it fails gracefully.

        async def mock_post(*args, **kwargs):
            url = args[0]
            json_body = kwargs.get('json', {})
            model = json_body.get('model')
            messages = json_body.get('messages')

            # Validation: Ensure messages is a list of dicts
            if not isinstance(messages, list) or not all(isinstance(m, dict) for m in messages):
                raise ValueError(f"Invalid messages payload format: {messages}")

            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.raise_for_status = MagicMock()

            if "gpt-4-turbo" in model:
                # Orchestrator
                content = '{"architecture_task": "Design scalable DB", "docs_task": "Find AWS docs", "frontend_task": "React UI"}'
            elif "gpt-5" in model:
                content = "Architecture is solid."
            elif "claude" in model:
                content = "Docs found."
            elif "gemini" in model:
                content = "UI Designed."
            else:
                content = "Synthesized response."

            mock_resp.json.return_value = {
                "choices": [{"message": {"content": content}}]
            }
            return mock_resp

        mock_client.post.side_effect = mock_post

        # Mock SimpleLLMNode Consul check (get request)
        async def mock_get(*args, **kwargs):
             mock_resp = MagicMock()
             mock_resp.status_code = 200
             mock_resp.raise_for_status = MagicMock()
             # Return fake service for SimpleLLMNode
             port = int(os.getenv("ROUTER_PORT", 8081))
             mock_resp.json.return_value = [{"Service": {"Address": "127.0.0.1", "Port": port}}]
             return mock_resp

        mock_client.get.side_effect = mock_get

        async def run_workflow():
            runner = WorkflowRunner(self.workflow_path)
            inputs = {
                "user_text": "Build me a super app.",
                "external_experts_config": MOCK_EXPERTS_CONFIG,
                "consul_http_addr": "http://localhost:8500"
            }
            result = await runner.run(inputs)
            return result

        result = asyncio.run(run_workflow())

        self.assertIn("Synthesized response", str(result))
        print("\nWorkflow Execution Result:", result)

if __name__ == '__main__':
    unittest.main()
