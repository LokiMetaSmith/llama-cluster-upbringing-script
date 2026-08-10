import logging
import asyncio
from typing import Optional, List

from pipecatapp.tools.atproto_sync.sync_buffer import PdsSyncBuffer
from pipecatapp.tools.atproto_sync.sync_worker import SyncWorker

logger = logging.getLogger(__name__)

class ATProtoTool:
    """
    A tool for interacting with the AT Protocol (Bluesky/Colibri) using the atproto SDK.
    Instead of broadcasting directly, actions like send_post are queued to a local sync buffer
    for eventual consistency.
    """
    def __init__(self, username: str, password: str, pds_url: str = "https://bsky.social", buffer_db_path: str = None):
        self.username = username
        self.password = password
        self.pds_url = pds_url
        self.description = "Queue public posts to the AT Protocol feed (broadcasts). Private agent thoughts must NOT be sent here."
        self.name = "atproto"
        self._client = None

        # Isolate the queue per identity so background workers don't cross-post if sharing a filesystem
        safe_username = "".join([c if c.isalnum() else "_" for c in self.username])
        actual_db_path = buffer_db_path if buffer_db_path else f"atproto_sync_{safe_username}.sqlite"

        # Initialize sync buffer and worker for local-first eventual consistency
        self.buffer = PdsSyncBuffer(db_path=actual_db_path)
        self.worker = SyncWorker(self.buffer, self._get_client, interval_seconds=30)

        # We start the worker immediately (or could delay until first action)
        # Note: If ATProtoTool is re-instantiated often, you might want a singleton worker,
        # but for this swarm integration, each agent/tool instance having a worker is acceptable.
        try:
            # We attempt to start it. It requires a running event loop.
            # In cases where it's initialized before the loop, we catch RuntimeError.
            loop = asyncio.get_running_loop()
            self.worker.start()
        except RuntimeError:
            pass # We can start it lazily on the first async call


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "atprototool"),
                "description": getattr(self, "description", "Tool ATProtoTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: send_post, get_timeline"
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Additional arguments for the action."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, **kwargs):
        # Ensure worker is started if we missed it during init
        if not self.worker._running:
            try:
                self.worker.start()
            except RuntimeError:
                pass

        if action == "send_post":
            return getattr(self, "send_post")(**kwargs.get("kwargs", kwargs))
        if action == "get_timeline":
            return getattr(self, "get_timeline")(**kwargs.get("kwargs", kwargs))
        else:
            return f"Unknown action: {action}"

    def _get_client(self):
        try:
            from atproto import Client
        except ImportError:
            raise ImportError("The 'atproto' package is not installed. Add it to requirements.txt.")

        if not self._client:
            self._client = Client(self.pds_url)
            self._client.login(self.username, self.password)
        return self._client

    async def send_post(self, text: str) -> str:
        """
        Queues a text post to the local sync buffer. It will be pushed to the PDS when online.

        Args:
            text (str): The content of the post.

        Returns:
            str: Result message indicating success or failure.
        """
        # Start worker if not started
        if not self.worker._running:
            self.worker.start()

        try:
            # We no longer block waiting for the remote PDS. We use the local buffer.
            event_id = self.buffer.add_event('send_post', {'text': text})
            if event_id != -1:
                return f"Post queued successfully for eventual broadcast (Local Event ID: {event_id})."
            else:
                return "Error: Failed to queue post locally."
        except Exception as e:
            logger.error(f"Error queueing post via AT Protocol: {e}")
            return f"Error queueing post: {str(e)}"

    async def get_timeline(self, limit: int = 10) -> str:
        """
        Fetches the latest posts from the user's timeline. Since this is a read operation,
        it still requires remote PDS connectivity.

        Args:
            limit (int): The maximum number of posts to fetch (default 10).

        Returns:
            str: A formatted string of the timeline posts or an error message.
        """
        try:
            client = await asyncio.to_thread(self._get_client)
            timeline = await asyncio.to_thread(client.get_timeline, limit=limit)

            posts = []
            for feed_view in timeline.feed:
                post = feed_view.post
                author_handle = post.author.handle
                # Some posts might not have text if they are just embeds, we handle basic text records
                if hasattr(post.record, 'text'):
                    text = post.record.text
                else:
                    text = "[No Text/Media Only]"

                posts.append(f"@{author_handle}: {text}")

            if not posts:
                return "Timeline is empty."

            return "\n".join(posts)

        except Exception as e:
            logger.error(f"Error fetching timeline via AT Protocol (offline?): {e}")
            return f"Could not fetch timeline. You might be offline or PDS is unreachable. Error: {str(e)}"
