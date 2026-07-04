import asyncio
import time
import requests
import aiohttp
import json
from unittest.mock import MagicMock, patch

# Implementation using requests (as described in the task)
class SyncLLMClient:
    def __init__(self, base_url, api_key, model):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

    def process_text_sync(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        # Simulate the synchronous call
        response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

# Current partially async implementation (from the file)
class CurrentAsyncLLMClient:
    def __init__(self, base_url, api_key, model):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self._session = None

    async def process_text(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        if not self._session:
            self._session = aiohttp.ClientSession()

        async with self._session.post(f"{self.base_url}/chat/completions", headers=headers, json=data) as response:
            response.raise_for_status()
            response_json = await response.json()
        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

async def benchmark_sync(client, num_requests):
    start_time = time.time()
    for i in range(num_requests):
        client.process_text_sync(f"prompt {i}")
    return time.time() - start_time

async def benchmark_async(client, num_requests):
    start_time = time.time()
    tasks = [client.process_text(f"prompt {i}") for i in range(num_requests)]
    await asyncio.gather(*tasks)
    return time.time() - start_time

def mock_response(*args, **kwargs):
    m = MagicMock()
    m.status_code = 200
    m.json.return_value = {"choices": [{"message": {"content": "mock response"}}]}
    m.raise_for_status = MagicMock()
    # Simulate network latency
    time.sleep(0.05)
    return m

async def run_benchmarks():
    num_requests = 20
    base_url = "http://mock-api.com"
    api_key = "test-key"
    model = "test-model"

    print(f"Running benchmarks with {num_requests} concurrent-like requests...")

    # Benchmark Sync
    sync_client = SyncLLMClient(base_url, api_key, model)
    with patch('requests.post', side_effect=mock_response):
        sync_duration = await benchmark_sync(sync_client, num_requests)
        print(f"Sync (requests) duration: {sync_duration:.4f}s")

    # Benchmark Current Async
    async_client = CurrentAsyncLLMClient(base_url, api_key, model)

    # We need to mock aiohttp differently
    class MockAsyncResponse:
        def __init__(self):
            self.status = 200
        async def __aenter__(self):
            await asyncio.sleep(0.05) # Simulate latency
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        def raise_for_status(self):
            pass
        async def json(self):
            return {"choices": [{"message": {"content": "mock response"}}]}

    with patch('aiohttp.ClientSession.post', return_value=MockAsyncResponse()):
        async_duration = await benchmark_async(async_client, num_requests)
        print(f"Async (aiohttp) duration: {async_duration:.4f}s")
        if async_client._session:
            await async_client._session.close()

    print(f"Improvement: {(sync_duration - async_duration) / sync_duration * 100:.2f}%")

if __name__ == "__main__":
    asyncio.run(run_benchmarks())
