import asyncio
import websockets
import json
import binascii

try:
    import pyaudio
    import opuslib
    HAS_AUDIO_LIBS = True
except ImportError:
    HAS_AUDIO_LIBS = False


class MockPyAudioStream:
    def __init__(self):
        pass

    def read(self, num_frames, exception_on_overflow=False):
        # Simulate some raw PCM audio data
        return b'\x00' * num_frames * 2 # 16-bit PCM = 2 bytes per frame


class PersonaPlexClient:
    def __init__(self, uri="ws://localhost:8080/stream", use_mock=False):
        self.uri = uri
        self.running = False

        self.use_mock = use_mock or not HAS_AUDIO_LIBS

        # Audio configuration
        self.chunk_size = 960  # Opus requires specific frame sizes (e.g., 960 at 48kHz for 20ms)
        self.format = pyaudio.paInt16 if HAS_AUDIO_LIBS else 8
        self.channels = 1
        self.rate = 48000

        if self.use_mock:
            self.stream = MockPyAudioStream()
            self.pyaudio_instance = None
            self.encoder = None
            self.decoder = None
        else:
            self.pyaudio_instance = pyaudio.PyAudio()
            self.stream = self.pyaudio_instance.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                output=True,
                frames_per_buffer=self.chunk_size
            )
            # Create Opus encoder and decoder for 48kHz, 1 channel
            self.encoder = opuslib.Encoder(self.rate, self.channels, opuslib.APPLICATION_AUDIO)
            self.decoder = opuslib.Decoder(self.rate, self.channels)

    async def _send_audio(self, websocket):
        while self.running:
            try:
                # Capture audio frame
                pcm_data = self.stream.read(self.chunk_size, exception_on_overflow=False)

                if not self.use_mock:
                    # Compress with Opus
                    compressed_data = self.encoder.encode(pcm_data, self.chunk_size)
                else:
                    compressed_data = pcm_data

                # Hex-encode the audio data for transmission
                hex_data = binascii.hexlify(compressed_data).decode('utf-8')

                payload = {
                    "type": "audio",
                    "data": hex_data
                }
                await websocket.send(json.dumps(payload))

                if self.use_mock:
                    await asyncio.sleep(self.chunk_size / self.rate) # Simulate audio capture interval
            except Exception as e:
                print(f"Error sending audio: {e}")
                self.running = False
                break

    async def _receive_audio(self, websocket):
        while self.running:
            try:
                response = await websocket.recv()
                data = json.loads(response)

                if data.get("type") == "audio":
                    # Hex-decode received audio
                    hex_data = data.get("data", "")
                    compressed_data = binascii.unhexlify(hex_data.encode('utf-8'))

                    if not self.use_mock:
                        # Decode with Opus
                        pcm_data = self.decoder.decode(compressed_data, self.chunk_size)

                        # Play back audio
                        self.stream.write(pcm_data)

            except Exception as e:
                print(f"Error receiving audio: {e}")
                self.running = False
                break

    async def start(self):
        self.running = True
        try:
            async with websockets.connect(self.uri) as websocket:
                send_task = asyncio.create_task(self._send_audio(websocket))
                receive_task = asyncio.create_task(self._receive_audio(websocket))

                await asyncio.gather(send_task, receive_task)
        except Exception as e:
            print(f"Connection error: {e}")
            self.running = False

    def stop(self):
        self.running = False
        if not self.use_mock:
            self.stream.stop_stream()
            self.stream.close()
            self.pyaudio_instance.terminate()
