import os
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import httpx

from pipecatapp.tools.jules_tool import JulesTool

class TestJulesTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.tool = JulesTool(api_key=self.api_key)
        self.prompt = "Fix the crash in the main loop"
        self.source = "sources/github/bobalover/boba"
        self.title = "Fix crash"

    async def test_run_success(self):
        # Mock httpx.AsyncClient and its post method
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "name": "sessions/12345",
            "id": "12345",
            "title": self.title,
            "sourceContext": {
                "source": self.source
            },
            "prompt": self.prompt
        }
        mock_response.raise_for_status.return_value = None

        mock_post = AsyncMock(return_value=mock_response)

        # We need to mock the context manager of AsyncClient
        mock_client = MagicMock()
        mock_client.post = mock_post
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)


        with patch('pipecatapp.tools.jules_tool.httpx.AsyncClient', return_value=mock_client):
            result = await self.tool.run(self.prompt, self.source, self.title)

        self.assertIn("Jules session created successfully", result)
        self.assertIn("Session ID: 12345", result)
        self.assertIn("Session Name: sessions/12345", result)

        # Verify POST was called with correct args
        mock_post.assert_called_once_with(
            "https://jules.googleapis.com/v1alpha/sessions",
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            },
            json={
                "prompt": self.prompt,
                "sourceContext": {"source": self.source},
                "title": self.title
            },
            timeout=30.0
        )

    async def test_run_missing_api_key(self):
        # Instantiate tool without API key
        with patch.dict(os.environ, clear=True):
            tool = JulesTool(api_key=None)
            result = await tool.run(self.prompt, self.source)
            self.assertEqual(result, "Error: JULES_API_KEY not configured.")

    async def test_run_http_error(self):
        # Create a mock exception that httpx would raise
        mock_request = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = '{"error": "Unauthorized"}'

        http_error = httpx.HTTPStatusError("Unauthorized", request=mock_request, response=mock_response)

        mock_post = AsyncMock(side_effect=http_error)

        mock_client = MagicMock()
        mock_client.post = mock_post
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)


        with patch('pipecatapp.tools.jules_tool.httpx.AsyncClient', return_value=mock_client):
            result = await self.tool.run(self.prompt, self.source)

        self.assertIn("Error creating Jules session: HTTP 401", result)
        self.assertIn('{"error": "Unauthorized"}', result)

    async def test_run_generic_exception(self):
        mock_post = AsyncMock(side_effect=Exception("Network failure"))

        mock_client = MagicMock()
        mock_client.post = mock_post
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)


        with patch('pipecatapp.tools.jules_tool.httpx.AsyncClient', return_value=mock_client):
            result = await self.tool.run(self.prompt, self.source)

        self.assertEqual(result, "Error executing Jules task: Network failure")

if __name__ == '__main__':
    unittest.main()
