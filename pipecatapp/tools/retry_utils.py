import asyncio
import functools
import logging
import random
import time
from dataclasses import dataclass
from typing import Callable, Optional, Set, Tuple, Type

logger = logging.getLogger(__name__)

@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True
    jitter_factor: float = 0.1

TRANSIENT_ERROR_MESSAGES: Set[str] = {
    "connection refused",
    "connection reset",
    "connection timed out",
    "temporary failure",
    "service unavailable",
    "resource temporarily unavailable",
    "too many requests",
    "rate limit",
    "docker daemon",
    "cannot connect to docker",
    "no space left on device",
}

def is_transient_error(error: Exception) -> bool:
    """Check if an error is likely transient and worth retrying."""
    error_msg = str(error).lower()
    for pattern in TRANSIENT_ERROR_MESSAGES:
        if pattern in error_msg:
            return True

    error_type = type(error).__name__.lower()
    transient_types = {"timeouterror", "connectionerror", "oserror", "clienterror"}
    if any(t in error_type for t in transient_types):
        return True

    return False

def calculate_delay(attempt: int, config: RetryConfig) -> float:
    """Calculate delay before next retry attempt using exponential backoff with optional jitter."""
    delay = config.base_delay * (config.exponential_base**attempt)
    delay = min(delay, config.max_delay)

    if config.jitter:
        jitter_range = delay * config.jitter_factor
        delay = delay + random.uniform(-jitter_range, jitter_range)

    return max(0, delay)

def retry(
    config: Optional[RetryConfig] = None,
    retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
):
    """Decorator for retrying a function with exponential backoff.
    Supports both synchronous and asynchronous functions.
    """
    if config is None:
        config = RetryConfig()

    if retryable_exceptions is None:
        retryable_exceptions = (Exception,)

    def decorator(func: Callable):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                last_exception = None

                for attempt in range(config.max_attempts):
                    try:
                        return await func(*args, **kwargs)
                    except retryable_exceptions as e:
                        last_exception = e

                        if attempt == config.max_attempts - 1:
                            logger.warning(f"Retry exhausted for {func.__name__} after {config.max_attempts} attempts: {e}")
                            raise

                        if not is_transient_error(e):
                            logger.debug(f"Non-transient error in {func.__name__}, not retrying: {e}")
                            raise

                        delay = calculate_delay(attempt, config)
                        logger.info(f"Retry {attempt + 1}/{config.max_attempts} for {func.__name__} after {delay:.2f}s: {e}")
                        await asyncio.sleep(delay)

                if last_exception:
                    raise last_exception

            return wrapper
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None

                for attempt in range(config.max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except retryable_exceptions as e:
                        last_exception = e

                        if attempt == config.max_attempts - 1:
                            logger.warning(f"Retry exhausted for {func.__name__} after {config.max_attempts} attempts: {e}")
                            raise

                        if not is_transient_error(e):
                            logger.debug(f"Non-transient error in {func.__name__}, not retrying: {e}")
                            raise

                        delay = calculate_delay(attempt, config)
                        logger.info(f"Retry {attempt + 1}/{config.max_attempts} for {func.__name__} after {delay:.2f}s: {e}")
                        time.sleep(delay)

                if last_exception:
                    raise last_exception

            return wrapper
    return decorator
