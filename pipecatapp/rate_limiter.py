import time
from collections import defaultdict, deque
from fastapi import Request, HTTPException, status

class RateLimiter:
    """
    Simple in-memory rate limiter using a sliding window algorithm.
    """
    def __init__(self, limit: int = 60, window: int = 60):
        """
        Initialize the rate limiter.

        Args:
            limit (int): Maximum number of requests allowed within the window.
            window (int): Time window in seconds.
        """
        self.limit = limit
        self.window = window
        # Dictionary to store request timestamps for each client IP
        self.requests: dict[str, deque] = defaultdict(deque)

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
