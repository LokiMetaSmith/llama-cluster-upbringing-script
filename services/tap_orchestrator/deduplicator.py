import time
import logging

logger = logging.getLogger(__name__)

class TapDeduplicator:
    def __init__(self, cooldown_seconds: int = 5):
        self.cooldown_seconds = cooldown_seconds
        self._last_tap: dict[str, float] = {}

    def is_allowed(self, user_id: str) -> bool:
        current_time = time.time()
        last_time = self._last_tap.get(user_id, 0)

        if current_time - last_time < self.cooldown_seconds:
            logger.warning(f"Tap ignored for {user_id}: cooldown active ({current_time - last_time:.2f}s < {self.cooldown_seconds}s)")
            return False

        self._last_tap[user_id] = current_time
        return True

deduplicator = TapDeduplicator()
