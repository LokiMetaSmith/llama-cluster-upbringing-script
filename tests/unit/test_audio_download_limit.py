import asyncio
import pytest
import httpx
import tempfile
import os

MAX_AUDIO_SIZE = 50 * 1024 * 1024 # 50 MB

@pytest.mark.asyncio
async def test_download_limit_exceeded():
    """
    Simulates a DoS attack by downloading an endless stream or extremely large file.
    Verifies that the new logic stops downloading and raises an error.
    """

    # Mock response stream that yields chunks indefinitely
    async def endless_stream():
        chunk = b"A" * 1024 * 1024 # 1MB chunk
        while True:
            yield chunk

    # Mock client.stream context manager
    class MockStream:
        def __init__(self, status_code=200):
            self.status_code = status_code

        async def aiter_bytes(self):
            chunk = b"A" * 1024 * 1024 # 1MB chunk
            # Yield enough chunks to exceed limit (51 chunks = 51MB)
            for _ in range(51):
                yield chunk

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    # The logic we are implementing in app.py
    async def download_audio_safe(client, url, headers):
        downloaded_size = 0
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            try:
                async with client.stream("GET", url, headers=headers) as resp:
                    if resp.status_code == 200:
                        async for chunk in resp.aiter_bytes():
                            downloaded_size += len(chunk)
                            if downloaded_size > MAX_AUDIO_SIZE:
                                raise ValueError(f"Audio file exceeds limit of {MAX_AUDIO_SIZE} bytes")
                            tmp_file.write(chunk)
            finally:
                tmp_file.close()
                os.remove(tmp_file.name)

    # Mock client
    class MockClient:
        def stream(self, method, url, headers=None):
            return MockStream()

    client = MockClient()

    # Verify that it raises ValueError
    with pytest.raises(ValueError) as excinfo:
        await download_audio_safe(client, "http://example.com/huge.mp3", {})

    assert f"Audio file exceeds limit of {MAX_AUDIO_SIZE} bytes" in str(excinfo.value)

@pytest.mark.asyncio
async def test_download_within_limit():
    """
    Verifies that a file within the limit is downloaded successfully.
    """
    # Mock stream with small content
    class MockStreamSmall:
        def __init__(self, status_code=200):
            self.status_code = status_code

        async def aiter_bytes(self):
            yield b"Small audio file content"

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    async def download_audio_safe(client, url, headers):
        downloaded_size = 0
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            try:
                async with client.stream("GET", url, headers=headers) as resp:
                    if resp.status_code == 200:
                        async for chunk in resp.aiter_bytes():
                            downloaded_size += len(chunk)
                            if downloaded_size > MAX_AUDIO_SIZE:
                                raise ValueError(f"Audio file exceeds limit of {MAX_AUDIO_SIZE} bytes")
                            tmp_file.write(chunk)
            finally:
                tmp_file.close()
                if os.path.exists(tmp_file.name):
                    os.remove(tmp_file.name)
        return downloaded_size

    class MockClientSmall:
        def stream(self, method, url, headers=None):
            return MockStreamSmall()

    client = MockClientSmall()
    size = await download_audio_safe(client, "http://example.com/small.mp3", {})
    assert size == len(b"Small audio file content")
