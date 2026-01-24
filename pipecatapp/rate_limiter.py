import time
from collections import defaultdict, deque
from fastapi import Request, HTTPException, status

class RateLimiter:
    """
    Simple in-memory rate limiter using a sliding window algorithm.
    """
    def __init__(self, limit: int = 60, window: int = 60, cleanup_interval: int = 600):
        """
        Initialize the rate limiter.

        Args:
            limit (int): Maximum number of requests allowed within the window.
            window (int): Time window in seconds.
            cleanup_interval (int): Interval in seconds to clean up expired keys.
        """
        self.limit = limit
        self.window = window
        self.cleanup_interval = cleanup_interval
        # Dictionary to store request timestamps for each client IP
        self.requests: dict[str, deque] = defaultdict(deque)
        self.last_cleanup = time.time()

    async def __call__(self, request: Request):
        """
        Check if the request is allowed.

        Args:
            request (Request): The incoming request.

        Raises:
            HTTPException: If the rate limit is exceeded.
        """
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Periodic cleanup to prevent memory leaks
        if now - self.last_cleanup > self.cleanup_interval:
            self._cleanup(now)

        # Get the deque of timestamps for this client
        timestamps = self.requests[client_ip]

        # Remove timestamps older than the window
        while timestamps and now - timestamps[0] > self.window:
            timestamps.popleft()

        # Check if limit is reached
        if len(timestamps) >= self.limit:
            wait_time = int(self.window - (now - timestamps[0]))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {wait_time} seconds."
            )

        # Add current timestamp
        timestamps.append(now)

    def _cleanup(self, now: float):
        """Removes expired entries from the requests dictionary."""
        self.last_cleanup = now
        # Iterate over a copy of keys to allow modification during iteration
        for ip in list(self.requests.keys()):
            dq = self.requests[ip]
            # Remove expired timestamps
            while dq and now - dq[0] > self.window:
                dq.popleft()
            # If deque is empty, remove the key
            if not dq:
                del self.requests[ip]
