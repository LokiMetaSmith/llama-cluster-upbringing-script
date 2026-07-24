import logging
import asyncio
import os
from typing import Optional, List

from atproto_sync_buffer import PdsSyncBuffer

logger = logging.getLogger(__name__)

class ATProtoTool:
    """
    A tool for interacting with the AT Protocol (Bluesky/Colibri) using the atproto SDK.
    Includes a local sync buffer for offline operations.
    """
    def __init__(self, username: str, password: str, pds_url: str = "https://bsky.social"):
        self.username = username
        self.password = password
        self.pds_url = pds_url
        self.description = "Read and send messages/posts via the AT Protocol (Bluesky/Colibri)."
        self.name = "atproto"
        self._client = None

        # Use an in-memory DB or local temp for testing if /opt is not writable, else use standard location
        db_path = "/opt/pipecatapp/atproto_buffer.db"
        if not os.path.exists("/opt/pipecatapp") or not os.access(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", os.W_OK):
             db_path = "atproto_buffer.db"

        self.sync_buffer = PdsSyncBuffer(db_path=db_path)

        # Start a background sync worker specifically for this handle if not already running
        try:
            loop = asyncio.get_running_loop()
            if not hasattr(loop, "_atproto_sync_workers_started"):
                loop._atproto_sync_workers_started = set()

            if self.username not in loop._atproto_sync_workers_started:
                loop._atproto_sync_workers_started.add(self.username)
                asyncio.create_task(self._background_sync_worker())
        except RuntimeError:
            logger.warning(f"No running asyncio event loop found during ATProtoTool initialization. Background sync for {self.username} will not start.")

    def _get_client(self):
        try:
            from atproto import Client
        except ImportError:
            raise ImportError("The 'atproto' package is not installed. Add it to requirements.txt.")

        if not self._client:
            self._client = Client(self.pds_url)
            self._client.login(self.username, self.password)
        return self._client

    async def _background_sync_worker(self):
        """
        Periodically checks the sync buffer and attempts to push pending posts to the remote PDS.
        """
        while True:
            try:
                # Only sync posts for the handle bound to this specific tool instance
                pending_posts = self.sync_buffer.get_pending_posts(self.username)
                if pending_posts:
                    client = await asyncio.to_thread(self._get_client)
                    for post in pending_posts:
                        try:
                            # Attempt to sync
                            await asyncio.to_thread(client.send_post, text=post['text'])
                            self.sync_buffer.mark_post_synced(post['id'])
                            logger.info(f"Successfully synced post {post['id']} to PDS from buffer for {self.username}.")
                        except Exception as e:
                            logger.warning(f"Failed to sync post {post['id']} to PDS during background sync: {e}")
                            break # Stop attempting to sync if network is down
            except Exception as e:
                logger.error(f"Error in ATProto background sync worker for {self.username}: {e}")

            await asyncio.sleep(60) # Check every 60 seconds

    async def send_post(self, text: str) -> str:
        """
        Sends a text post via the AT Protocol.
        If the PDS is unreachable, it queues the post in the local sync buffer for eventual consistency.

        Args:
            text (str): The content of the post.

        Returns:
            str: Result message indicating success or offline buffering.
        """
        # Always enqueue first to ensure we don't lose the data
        post_id = self.sync_buffer.enqueue_post(text, self.username)

        try:
            # Attempt immediate sync
            client = await asyncio.to_thread(self._get_client)
            result = await asyncio.to_thread(client.send_post, text=text)
            self.sync_buffer.mark_post_synced(post_id)
            return f"Post sent successfully. URI: {result.uri}"
        except Exception as e:
            logger.warning(f"PDS unreachable. Post buffered locally. Error: {e}")
            return f"PDS unreachable. Post buffered locally for later sync (ID: {post_id})."

    async def get_timeline(self, limit: int = 10) -> str:
        """
        Fetches the latest posts from the user's timeline.

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
            logger.error(f"Error fetching timeline via AT Protocol: {e}")
            return f"Error fetching timeline: {str(e)}"
