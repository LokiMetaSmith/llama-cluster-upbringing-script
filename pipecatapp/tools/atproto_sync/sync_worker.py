import asyncio
import logging
from typing import Any, Optional

from pipecatapp.tools.atproto_sync.sync_buffer import PdsSyncBuffer

logger = logging.getLogger(__name__)


class SyncWorker:
    """
    A background worker that periodically polls the PdsSyncBuffer for pending
    ATProto actions (e.g., 'send_post') and attempts to execute them using the
    provided client initialization function.
    Provides eventual consistency for offline publishing.
    """

    def __init__(self, buffer: PdsSyncBuffer, get_client_func, interval_seconds: int = 15):
        self.buffer = buffer
        self.get_client_func = get_client_func
        self.interval_seconds = interval_seconds
        self._running = False
        self._task: Optional[asyncio.Task] = None

    def start(self):
        """Starts the background synchronization loop."""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._sync_loop())
        logger.info("ATProto SyncWorker started.")

    def stop(self):
        """Stops the background synchronization loop."""
        self._running = False
        if self._task:
            self._task.cancel()
        logger.info("ATProto SyncWorker stopped.")

    async def _sync_loop(self):
        """Main loop that polls and processes pending events."""
        while self._running:
            try:
                events = self.buffer.get_pending_events()
                if events:
                    logger.info(f"SyncWorker found {len(events)} pending ATProto events.")
                    await self._process_events(events)
            except Exception as e:
                logger.error(f"Error in SyncWorker loop: {e}")

            await asyncio.sleep(self.interval_seconds)

    async def _process_events(self, events: list):
        """Processes a list of pending events."""
        # Try to initialize the client. If it fails (e.g., offline), we skip processing
        # this batch and wait for the next loop.
        try:
            client = await asyncio.to_thread(self.get_client_func)
        except Exception as e:
            logger.warning(f"SyncWorker could not get ATProto client (offline/unreachable PDS). Retrying later. Error: {e}")
            return

        for event in events:
            event_id = event['id']
            action = event['action']
            payload = event['payload']

            try:
                if action == 'send_post':
                    text = payload.get('text', '')
                    # Execute the client action in a separate thread to prevent blocking
                    await asyncio.to_thread(client.send_post, text=text)
                    self.buffer.mark_event_completed(event_id)
                    logger.info(f"SyncWorker successfully completed event {event_id} ({action}).")
                else:
                    error_msg = f"Unknown action: {action}"
                    logger.error(error_msg)
                    self.buffer.mark_event_failed(event_id, error_msg)

            except Exception as e:
                # If an individual event fails, we check if it's a network error vs a hard format error.
                # For simplicity, we can assume if the PDS is unreachable, it raises an Exception,
                # and we might just leave it pending to retry next time, or we can use error matching.
                # Here we will leave it pending if it fails (eventual consistency).
                logger.warning(f"SyncWorker failed to process event {event_id} ({action}): {e}. Will retry.")
