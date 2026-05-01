# Plan to Fix TODO Item

1. **Fix FastAPI Mocking**: Ensure FastAPI and `fastapi.responses` are properly mocked in test collection so `app.py` doesn't crash test discovery.
   - I will add `fastapi.responses` and `pmm_memory` to the `modules_to_mock` list in `tests/unit/conftest.py`.
   - I will verify this fixes test discovery in `tests/unit/test_pipecat_app_unit.py`.
   - I will update `TODO.md` to check off only this specific item to follow the instructions precisely.
