
import unittest
import io
import wave
import struct
import base64
import json
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from pipecat.frames.frames import AudioRawFrame

# Mock web_server before importing app to avoid circular import issues or missing dependencies
import sys
mock_web_server = MagicMock()
mock_web_server.manager = MagicMock()
mock_web_server.manager.broadcast = AsyncMock()
sys.modules["web_server"] = mock_web_server

# Now we can import WebsocketAudioStreamer from app
# We need to mock other dependencies that app.py imports
sys.modules["ultralytics"] = MagicMock()
sys.modules["faster_whisper"] = MagicMock()
sys.modules["piper"] = MagicMock()
sys.modules["piper.voice"] = MagicMock()
sys.modules["consul"] = MagicMock()
sys.modules["consul.aio"] = MagicMock()
sys.modules["numpy"] = MagicMock()

# Mocking internal modules
# sys.modules["pipecat.frames.frames"] = MagicMock() # already imported
# from pipecat.frames.frames import AudioRawFrame

# Re-import app to get the class
from pipecatapp.app import WebsocketAudioStreamer

class TestWebsocketAudioStreamer(unittest.IsolatedAsyncioTestCase):
    async def test_websocket_audio_streamer_wav_header(self):
        """Test that WebsocketAudioStreamer correctly packs audio into WAV format."""

        streamer = WebsocketAudioStreamer(sample_rate=16000)

        # Create a dummy audio frame (16-bit PCM, mono)
        # 20ms of silence
        audio_data = b'\x00\x00' * 320
        frame = AudioRawFrame(audio=audio_data)

        # Mock push_frame to avoid downstream effects
        streamer.push_frame = AsyncMock()

        # Reset mock
        mock_web_server.manager.broadcast.reset_mock()

        await streamer.process_frame(frame, direction=None)

        # Verify broadcast was called
        self.assertTrue(mock_web_server.manager.broadcast.called)

        # Get arguments
        call_args = mock_web_server.manager.broadcast.call_args
        message_json = call_args[0][0]
        message = json.loads(message_json)

        self.assertEqual(message["type"], "audio")
        b64_audio = message["data"]

        # Decode base64
        wav_bytes = base64.b64decode(b64_audio)

        # Verify WAV header
        # Check RIFF
        self.assertEqual(wav_bytes[0:4], b'RIFF')
        # Check WAVE
        self.assertEqual(wav_bytes[8:12], b'WAVE')
        # Check fmt
        self.assertEqual(wav_bytes[12:16], b'fmt ')
        # Check data
        self.assertIn(b'data', wav_bytes)

        # Verify content using wave module
        wav_buffer = io.BytesIO(wav_bytes)
        with wave.open(wav_buffer, "rb") as wf:
            self.assertEqual(wf.getnchannels(), 1)
            self.assertEqual(wf.getsampwidth(), 2)
            self.assertEqual(wf.getframerate(), 16000)
            read_frames = wf.readframes(wf.getnframes())
            self.assertEqual(read_frames, audio_data)

if __name__ == "__main__":
    unittest.main()
