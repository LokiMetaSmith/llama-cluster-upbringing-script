import asyncio
import time
import sys

# add path
import os
sys.path.insert(0, os.path.abspath('.'))

from pipecatapp.llm_clients import ExternalLLMClient
from unittest.mock import patch, MagicMock

async def main():
    client = ExternalLLMClient("http://fake.url", "fake_key", "fake_model")

    # We will mock requests.post to simulate a delay of 0.1s
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"message": {"content": "Hello"}}]}

        def fake_post(*args, **kwargs):
            time.sleep(0.1)
            return mock_response

        mock_post.side_effect = fake_post

        start_time = time.time()
        # run 10 concurrent requests
        tasks = [client.process_text("test") for _ in range(10)]
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        print(f"Time taken for 10 requests: {end_time - start_time:.2f} seconds")
        print(f"Results: {results[0]}")

if __name__ == "__main__":
    asyncio.run(main())
