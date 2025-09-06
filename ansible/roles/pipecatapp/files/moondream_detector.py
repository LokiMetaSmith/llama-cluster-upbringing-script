from transformers import AutoModelForCausalLM
from PIL import Image
import torch
from pipecat.processors.frame_processor import FrameProcessor
from pipecat.frames.frames import VisionImageFrame

class MoondreamDetector(FrameProcessor):
    def __init__(self, model_name="vikhyatk/moondream2", revision="2025-01-09"):
        super().__init__()
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            revision=revision,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            # Use CUDA if available, otherwise CPU
            device_map={"": "cuda"} if torch.cuda.is_available() else {"": "cpu"}
        )
        self.latest_observation = "I don't see anything."
        print("MoondreamDetector initialized.")

    async def process_frame(self, frame, direction):
        if not isinstance(frame, VisionImageFrame):
            await self.push_frame(frame, direction)
            return

        try:
            # Generate a caption for the image.
            caption = self.model.caption(frame.image, length="short")["caption"]

            # Only update if the observation has changed to avoid spamming logs.
            if caption and caption != self.latest_observation:
                self.latest_observation = caption
                print(f"MoondreamDetector updated observation: {self.latest_observation}")
        except Exception as e:
            print(f"Error in MoondreamDetector: {e}")
            self.latest_observation = "I am having trouble seeing."

        # This processor's purpose is to maintain a state (`latest_observation`).
        # It doesn't need to push any frames downstream.

    def get_observation(self):
        """
        Gets a real-time description of what is visible in the webcam.
        """
        return self.latest_observation
