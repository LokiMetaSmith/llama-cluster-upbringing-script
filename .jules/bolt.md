## 2024-05-23 - Blocking Inference in AsyncIO
**Learning:** Even "fast" model inference (0.1s) blocks the asyncio event loop if not offloaded to a thread, causing the entire application to stutter.
**Action:** Always wrap `self.model.generate()` or similar HF calls in `loop.run_in_executor`, even if they seem fast.

## 2024-05-23 - Rate Limiting Vision
**Learning:** Continuous vision processing (30fps) is unnecessary for "observation" agents and wastes resources.
**Action:** Implement explicit 1 FPS throttling for vision inputs unless real-time tracking is strictly required.

## 2025-11-26 - Zero-Copy Audio Buffering
**Learning:** Using `bytes(bytearray)` creates an unnecessary copy. `bytearray` can be swapped and passed directly to `np.frombuffer` which supports the buffer interface.
**Action:** When buffering data for processing in another thread, swap the buffer reference (e.g. `buf = self.b; self.b = bytearray()`) instead of copying it if the consumer supports the buffer interface.
