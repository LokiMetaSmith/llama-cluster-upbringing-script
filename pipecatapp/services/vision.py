import asyncio
import base64
import json
import logging
import os
import time

import cv2

# Set config dir before importing ultralytics to avoid permission errors
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"
from pipecat.frames.frames import UserImageRawFrame as VisionImageRawFrame
from pipecat.processors.frame_processor import FrameProcessor

from pipecatapp.moondream_detector import MoondreamDetector

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None
    logging.warning("Ultralytics not found. YOLOv8 vision will be disabled.")

class YOLOv8Detector(FrameProcessor):
    """A Pipecat processor for real-time object detection using YOLOv8.

    This processor analyzes incoming video frames to detect objects and maintains
    a textual description of the current scene.

    Attributes:
        model: The loaded YOLOv8 model.
        latest_observation (str): A human-readable string of detected objects.
        last_detected_objects (set): The set of objects detected in the last frame.
    """
    def __init__(self):
        """Initializes the YOLOv8 detector."""
        super().__init__()
        model_path = os.getenv("YOLO_MODEL_PATH")
        if not model_path:
             logging.error("YOLO_MODEL_PATH environment variable not set.")
             model_path = "/opt/nomad/models/vision/yolov8n.pt" # Last resort fallback
        self.latest_observation = "I don't see anything."
        self.last_detected_objects = set()
        self.last_processed_time = 0
        self.is_processing = False
        self.connection_check_callback = None

        if YOLO is None:
             logging.error("YOLOv8 model unavailable because ultralytics module is missing.")
             self.model = None
             self.latest_observation = "Vision system unavailable (missing dependency)."
             return

        try:
            self.model = YOLO(model_path)
        except Exception as e:
            logging.error(f"Failed to load YOLOv8 model from {model_path}: {e}")
            self.model = None
            self.latest_observation = "Vision system unavailable."

    def set_connection_check_callback(self, callback):
        """Sets a callback to check if there are active connections.

        Args:
            callback (callable): A function that returns True if debug images should be generated.
        """
        self.connection_check_callback = callback

    def _run_inference(self, image, generate_debug_image=False):
        """Helper to run inference in a separate thread.

        Args:
            image: The image data to process.
            generate_debug_image (bool): Whether to generate a base64 debug image.

        Returns:
            tuple: (set of detected object names, base64_encoded_jpeg_string)
        """
        results = self.model(image)
        detected_objects = {self.model.names[int(c)] for r in results for c in r.boxes.cls}

        # Generate visual debug frame
        img_base64 = None
        if generate_debug_image:
            try:
                # Plot returns a numpy array (BGR)
                annotated_frame = results[0].plot()

                # Bolt ⚡ Optimization: Use OpenCV for faster JPEG encoding (avoid PIL & extra allocations)
                # annotated_frame is BGR. cv2.imencode expects BGR.
                success, buffer = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                if success:
                    img_base64 = base64.b64encode(buffer).decode('utf-8')
            except Exception as e:
                logging.error(f"Error generating visual debug frame: {e}")

        return detected_objects, img_base64

    async def process_frame(self, frame, direction):
        """Processes an image frame to detect objects.

        Args:
            frame: The image frame to process.
            direction: The direction of the frame in the pipeline.
        """
        if not isinstance(frame, VisionImageRawFrame):
            await self.push_frame(frame, direction)
            return

        if self.model is None:
            # Pass frame through without processing if vision is unavailable
            await self.push_frame(frame, direction)
            return

        current_time = time.time()
        # Bolt ⚡ Optimization: Rate limit to 1 FPS and avoid concurrent processing
        if (current_time - self.last_processed_time < 1.0) or self.is_processing:
            await self.push_frame(frame, direction)
            return

        self.is_processing = True
        self.last_processed_time = current_time

        try:
            # Bolt ⚡ Optimization: Check if anyone is watching to avoid expensive image encoding
            generate_debug_image = True
            if self.connection_check_callback:
                try:
                    generate_debug_image = self.connection_check_callback()
                except Exception as e:
                    logging.warning(f"Connection check callback failed: {e}")
                    generate_debug_image = True

            loop = asyncio.get_running_loop()
            # Bolt ⚡ Optimization: Run blocking inference in a thread
            detected_objects, img_base64 = await loop.run_in_executor(
                None, self._run_inference, frame.image, generate_debug_image
            )

            # Broadcast visual debug frame
            if img_base64:
                # Fix: Import web_server locally to avoid NameError and circular dependencies
                try:
                    import pipecatapp.web_server
                    await pipecatapp.web_server.manager.broadcast(json.dumps({
                        "type": "vision_debug",
                        "data": img_base64
                    }))
                except Exception as ws_err:
                     logging.error(f"Failed to broadcast vision frame: {ws_err}")

        except Exception as e:
            logging.error(f"YOLOv8 detection error: {e}")
            detected_objects = set()
        finally:
            self.is_processing = False

        if detected_objects != self.last_detected_objects:
            self.last_detected_objects = detected_objects
            self.latest_observation = f"I see {', '.join(detected_objects)}." if detected_objects else "I don't see anything."
            logging.info(f"YOLOv8Detector updated observation: {self.latest_observation}")

    def get_observation(self) -> str:
        """Returns the latest observation of detected objects.

        Returns:
            A string describing the objects currently visible.
        """
        return self.latest_observation


def initialize_vision_detector(app_config: dict) -> FrameProcessor:
    """Initializes the vision detector based on configuration with failover.

    This function selects a primary vision model (e.g., YOLOv8, Moondream)
    based on the `app_config`. If the primary model fails to initialize,
    it attempts to load a fallback model. If both fail, it returns a dummy
    processor that indicates the vision system is unavailable.

    Args:
        app_config (dict): The application configuration dictionary.

    Returns:
        An instance of a vision detector (e.g., YOLOv8Detector, MoondreamDetector)
        or a dummy FrameProcessor if initialization fails.
    """
    vision_model_name = app_config.get("vision_model", "yolov8")
    primary_model, fallback_model = (YOLOv8Detector, MoondreamDetector) if vision_model_name == "yolov8" else (MoondreamDetector, YOLOv8Detector)

    try:
        logging.info(f"Attempting to initialize primary vision model: {primary_model.__name__}")
        detector = primary_model()
        logging.info(f"Successfully initialized {primary_model.__name__}")
        return detector
    except Exception as e:
        logging.warning(f"Failed to initialize {primary_model.__name__}: {e}. Attempting fallback.")
        try:
            logging.info(f"Attempting to initialize fallback vision model: {fallback_model.__name__}")
            detector = fallback_model()
            logging.info(f"Successfully initialized {fallback_model.__name__}")
            return detector
        except Exception as e_fallback:
            logging.error(f"Failed to initialize fallback vision model {fallback_model.__name__}: {e_fallback}")
            class VisionUnavailable(FrameProcessor):
                def get_observation(self) -> str:
                    return "Vision system is completely unavailable."
            detector = VisionUnavailable()
            logging.info("Initialized with a dummy vision processor.")
            return detector
