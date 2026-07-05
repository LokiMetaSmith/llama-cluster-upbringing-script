import pytest
import backon
import asyncio
from pipecatapp.utils.backon_utils import is_transient_error, retry_if_transient

def test_is_transient_error():
    # Test message-based detection
    assert is_transient_error(Exception("Connection refused")) is True
    assert is_transient_error(Exception("Something went wrong")) is False
    assert is_transient_error(Exception("Rate limit exceeded")) is True
    assert is_transient_error(Exception("No space left on device")) is True

    # Test type-based detection
    assert is_transient_error(TimeoutError("Timeout")) is True
    assert is_transient_error(ConnectionError("Conn error")) is True

    # Test "clienterror" type name detection
    class MyClientError(Exception):
        pass
    assert is_transient_error(MyClientError("client error")) is True

@pytest.mark.asyncio
async def test_backon_retry_with_transient_predicate():
    attempts = 0

    async def failing_func():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception("Connection refused")
        return "success"

    result = await backon.retry(
        failing_func,
        backon.constant,
        exception=Exception,
        max_tries=3,
        interval=0.01,
        condition=retry_if_transient
    )

    assert result == "success"
    assert attempts == 3

@pytest.mark.asyncio
async def test_backon_no_retry_on_non_transient():
    attempts = 0

    async def critical_failure_func():
        nonlocal attempts
        attempts += 1
        raise Exception("Critical permanent error")

    with pytest.raises(Exception, match="Critical permanent error"):
        await backon.retry(
            critical_failure_func,
            backon.constant,
            exception=Exception,
            max_tries=3,
            interval=0.01,
            condition=retry_if_transient
        )

    # Should only attempt once because it's not a transient error according to our predicate
    assert attempts == 1

@pytest.mark.asyncio
async def test_backon_retrying_context_manager():
    attempts = 0

    async def failing_func():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise Exception("connection reset")
        return "ok"

    async with backon.Retrying(backon.constant, exception=Exception, interval=0.01, condition=retry_if_transient) as r:
        result = await r.async_call(failing_func)

    assert result == "ok"
    assert attempts == 2
