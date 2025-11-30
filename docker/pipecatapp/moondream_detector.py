from transformers import AutoModelForCausalLM
import torch
from pipecat.processors.frame_processor import FrameProcessor
from pipecat.frames.frames import UserImageRawFrame as VisionImageRawFrame

class MoondreamDetector(FrameProcessor):
    """A vision processor that generates textual descriptions of image frames.

    This class uses the Moondream2 model to caption incoming `VisionImageRawFrame`
    objects. It runs in a parallel pipeline to continuously update its internal
    state (`latest_observation`) with a description of what it "sees".

    Attributes:
        model: The loaded Moondream2 model for image captioning.
        latest_observation (str): The most recent textual description of a
            processed image frame.
    """
    def __init__(self):
        """Initializes the MoondreamDetector.

        Loads the Moondream2 model from a predefined path and sets the device
        (CUDA if available, otherwise CPU).
        """
        super().__init__()
        # The model is now managed by Ansible and placed in a predictable location.
        model_path = "/opt/nomad/models/vision/moondream2"
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            # Use CUDA if available, otherwise CPU
            device_map={"": "cuda"} if torch.cuda.is_available() else {"": "cpu"}
        )
        self.latest_observation = "I don't see anything."
        print("MoondreamDetector initialized.")

    async def process_frame(self, frame, direction):
        """Processes a vision frame to generate and store a caption.

        If the frame is a `VisionImageRawFrame`, it generates a short caption
        and updates the `latest_observation` attribute. This processor does not
        push any frames downstream; its sole purpose is to maintain the
        observation state.

        Args:
            frame: The frame to process from the pipeline.
            direction: The direction of the frame in the pipeline.
        """
        if not isinstance(frame, VisionImageRawFrame):
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

    def get_observation(self) -> str:
        """Gets a real-time description of what is visible in the webcam.

        This method is called by other services to get the agent's current
        visual understanding of its environment.

        Returns:
            str: The latest observation as a text string.
        """
        return self.latest_observation