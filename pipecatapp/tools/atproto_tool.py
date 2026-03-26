import logging
import asyncio
from typing import Optional, List

logger = logging.getLogger(__name__)

class ATProtoTool:
    """
    A tool for interacting with the AT Protocol (Bluesky/Colibri) using the atproto SDK.
    """
    def __init__(self, username: str, password: str, pds_url: str = "https://bsky.social"):
        self.username = username
        self.password = password
        self.pds_url = pds_url
        self.description = "Read and send messages/posts via the AT Protocol (Bluesky/Colibri)."
        self.name = "atproto"
        self._client = None

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
        Sends a text post via the AT Protocol.

        Args:
            text (str): The content of the post.

        Returns:
            str: Result message indicating success or failure.
        """
        try:
            # We run the synchronous atproto Client in a thread to avoid blocking the event loop
            client = await asyncio.to_thread(self._get_client)
            result = await asyncio.to_thread(client.send_post, text=text)
            return f"Post sent successfully. URI: {result.uri}"
        except Exception as e:
            logger.error(f"Error sending post via AT Protocol: {e}")
            return f"Error sending post: {str(e)}"

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
