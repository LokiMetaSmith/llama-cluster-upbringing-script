import asyncio
import logging

from pipecat.frames.frames import EndFrame, TextFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.elevenlabs import ElevenLabsTTSService
from pipecat.services.openai import OpenAILLMService
from pipecat.transports.local.local import LocalTransport

logging.basicConfig(level=logging.DEBUG)

async def main():
    transport = LocalTransport()

    stt = DeepgramSTTService()
    llm = OpenAILLMService(
        base_url="http://localhost:8080/v1", # This should point to the prima.cpp service
        api_key="dummy",
        model="dummy"
    )
    tts = ElevenLabsTTSService(
        voice_id="21m00Tcm4TlvDq8ikWAM" # A default voice
    )

    pipeline = Pipeline([
        transport.input(),
        stt,
        llm,
        tts,
        transport.output()
    ])

    task = PipelineTask(pipeline)

    # A simple way to handle interruption
    async def handle_interrupt(frame):
        if isinstance(frame, TextFrame) and frame.text.strip():
            logging.info(f"User interrupted with: {frame.text}")
            await task.cancel()

    # Create a simple interruption pipeline
    interrupt_pipeline = Pipeline([
        transport.input(),
        stt,
        PipelineTask(handle_interrupt)
    ])

    runner = PipelineRunner()

    await runner.run(
        [task, PipelineTask(interrupt_pipeline)]
    )

if __name__ == "__main__":
    asyncio.run(main())
