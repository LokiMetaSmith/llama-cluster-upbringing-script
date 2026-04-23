import asyncio
from typing import Optional
from pydantic import BaseModel
from loguru import logger

from pipecat.services.llm_service import LLMService, LLMContext
from pipecat.frames.frames import TextFrame, LLMFullResponseEndFrame, LLMFullResponseStartFrame
from pipecat.adapters.services.open_ai_adapter import OpenAILLMAdapter

class LocalLLMService(LLMService):
    """
    A local LLM service that natively integrates llama-cpp-python directly with Pipecat's
    LLMService interface, without spawning a background HTTP server.
    """
    adapter_class = OpenAILLMAdapter

    class Settings(BaseModel):
        model: Optional[str] = "local"
        system_instruction: Optional[str] = None

    _settings: Settings

    def __init__(self, model_path: str, **kwargs):
        from llama_cpp import Llama

        self.model_path = model_path
        logger.info(f"Initializing native llama-cpp bindings with model: {self.model_path}")
        self._model = Llama(
            model_path=self.model_path,
            n_gpu_layers=-1,
            verbose=False
        )

        default_settings = self.Settings(model=model_path)
        super().__init__(settings=default_settings, **kwargs)

    async def _process_context(self, context: LLMContext):
        adapter = self.get_llm_adapter()
        params = adapter.get_llm_invocation_params(
            context,
            system_instruction=self._settings.system_instruction,
            convert_developer_to_user=True
        )
        messages = params.messages

        await self.push_frame(LLMFullResponseStartFrame())

        loop = asyncio.get_running_loop()
        stream = await loop.run_in_executor(
            None,
            lambda: self._model.create_chat_completion(
                messages=messages,
                stream=True
            )
        )

        while True:
            try:
                # get next chunk in a thread pool to avoid blocking the event loop
                chunk = await loop.run_in_executor(None, next, stream)

                if "choices" in chunk and len(chunk["choices"]) > 0:
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        await self.push_frame(TextFrame(content))
            except StopIteration:
                break

        await self.push_frame(LLMFullResponseEndFrame())

    async def run_inference(
        self,
        context: LLMContext,
        max_tokens: Optional[int] = None,
        system_instruction: Optional[str] = None,
    ) -> Optional[str]:
        effective_instruction = system_instruction or self._settings.system_instruction
        adapter = self.get_llm_adapter()
        params = adapter.get_llm_invocation_params(
            context,
            system_instruction=effective_instruction,
            convert_developer_to_user=True
        )
        messages = params.messages

        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self._model.create_chat_completion(
                messages=messages,
                stream=False
            )
        )

        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0].get("message", {}).get("content", "")
        return None
