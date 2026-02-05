## 2024-05-23 - Blocking Inference in AsyncIO
**Learning:** Even "fast" model inference (0.1s) blocks the asyncio event loop if not offloaded to a thread, causing the entire application to stutter.
**Action:** Always wrap `self.model.generate()` or similar HF calls in `loop.run_in_executor`, even if they seem fast.

## 2024-05-23 - Rate Limiting Vision
**Learning:** Continuous vision processing (30fps) is unnecessary for "observation" agents and wastes resources.
**Action:** Implement explicit 1 FPS throttling for vision inputs unless real-time tracking is strictly required.

## 2025-11-26 - Zero-Copy Audio Buffering
**Learning:** Using `bytes(bytearray)` creates an unnecessary copy. `bytearray` can be swapped and passed directly to `np.frombuffer` which supports the buffer interface.
**Action:** When buffering data for processing in another thread, swap the buffer reference (e.g. `buf = self.b; self.b = bytearray()`) instead of copying it if the consumer supports the buffer interface.

## 2026-01-24 - In-place Numpy Operations
**Learning:** Performing arithmetic operations in-place (e.g., `*=`) on Numpy arrays avoids allocating temporary arrays, significantly reducing memory churn and CPU time for large buffers.
**Action:** Use in-place operators for element-wise operations on large arrays whenever possible.

## 2025-06-15 - Redundant JSON Serialization Checks
**Learning:** Using `try: json.dumps(val)` just to check if a value is serializable is incredibly expensive for large strings (e.g. LLM outputs), as it re-encodes the entire string.
**Action:** Add a type check fast-path for primitives (str, int, bool) before attempting complex serialization checks.

## 2025-05-27 - Fast Path Regex vs Loop
**Learning:** Iterating through a list of strings with `any(sub in text for sub in list)` to skip expensive operations is O(N*M) where M is the number of triggers. For M=15, a single compiled Regex (O(N)) is ~2.8x faster on short strings.
**Action:** When implementing fast-path checks with multiple triggers, verify if a combined Regex is faster than a loop, especially if the loop size is > 5.

## 2026-02-04 - Recursive Type Check vs JSON Dump
**Learning:** `json.dumps(obj)` validates serialization by processing the entire string content. For objects containing large strings (like LLM outputs), this is O(total_chars). A recursive `isinstance` check is O(structure_size) and avoids processing string content, offering >1000x speedup for large payloads.
**Action:** Replace `try: json.dumps(obj)` validation checks with a recursive `make_serializable` helper that traverses the structure and stringifies only non-serializable leaves.

## 2026-02-18 - Single-Pass Serialization and Sanitization
**Learning:** Applying data sanitization (redaction) as a separate pass after object serialization causes double traversal and memory allocation. Combining them into a single recursive function reduces overhead by ~40% for large nested structures.
**Action:** Integrate sanitization logic directly into the serialization/traversal function using an optional flag instead of wrapping the result.
