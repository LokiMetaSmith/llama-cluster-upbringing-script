import asyncio
import time
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from pipecatapp.llm_clients import ExternalLLMClient
from unittest.mock import patch, MagicMock, AsyncMock

async def main():
    client = ExternalLLMClient("http://fake.url", "fake_key", "fake_model")

    # We will mock aiohttp.ClientSession.post to simulate a delay of 0.1s
    with patch('aiohttp.ClientSession.post') as mock_post:

        class AsyncContextManagerMock:
            async def __aenter__(self):
                await asyncio.sleep(0.1)
                mock_resp = MagicMock()
                mock_resp.json = AsyncMock(return_value={"choices": [{"message": {"content": "Hello"}}]})
                return mock_resp
            async def __aexit__(self, exc_type, exc_val, exc_tb):
                pass

        # side_effect returning a new instance on each call
        mock_post.side_effect = lambda *args, **kwargs: AsyncContextManagerMock()

        start_time = time.time()
        # run 10 concurrent requests
        tasks = [client.process_text("test") for _ in range(10)]
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        print(f"Time taken for 10 requests: {end_time - start_time:.2f} seconds")
        print(f"Results: {results[0]}")

    if client._session:
        await client._session.close()

if __name__ == "__main__":
    asyncio.run(main())
