## 2024-05-23 - Blocking Inference in AsyncIO
**Learning:** Even "fast" model inference (0.1s) blocks the asyncio event loop if not offloaded to a thread, causing the entire application to stutter.
**Action:** Always wrap `self.model.generate()` or similar HF calls in `loop.run_in_executor`, even if they seem fast.

## 2024-05-23 - Rate Limiting Vision
**Learning:** Continuous vision processing (30fps) is unnecessary for "observation" agents and wastes resources.
**Action:** Implement explicit 1 FPS throttling for vision inputs unless real-time tracking is strictly required.
