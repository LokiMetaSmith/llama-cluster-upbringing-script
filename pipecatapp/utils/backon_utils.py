import logging
import backon
from typing import Any

logger = logging.getLogger(__name__)

# Transient error patterns migrated from retry_utils.py
TRANSIENT_ERROR_MESSAGES = {
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

TRANSIENT_EXCEPTION_TYPES = (
    TimeoutError,
    ConnectionError,
    OSError,
    # Many libraries have their own ClientError, but we'll stick to built-ins
    # or handle them via predicate if needed.
)

def is_transient_error(exc: Exception) -> bool:
    """Predicate to determine if an exception is transient."""
    error_msg = str(exc).lower()
    if any(pattern in error_msg for pattern in TRANSIENT_ERROR_MESSAGES):
        return True

    if isinstance(exc, TRANSIENT_EXCEPTION_TYPES):
        return True

    # Check for "clienterror" in type name as done in original retry_utils
    if "clienterror" in type(exc).__name__.lower():
        return True

    return False

# Backon retry condition for transient errors
retry_if_transient = backon.retry_if_exception(is_transient_error)

class MultiMetricsCollector:
    # Modified to not inherit from backon.MetricsCollector as it doesn't exist in this version
    """Collector that dispatches to multiple backon metrics collectors."""
    def __init__(self, collectors):
        self.collectors = collectors

    def emit_attempt(self, tries: int, elapsed: float, target_name: str, exception_type: str | None = None) -> None:
        for c in self.collectors:
            try:
                c.emit_attempt(tries, elapsed, target_name, exception_type)
            except Exception:
                pass

    def emit_success(self, tries: int, elapsed: float, target_name: str) -> None:
        for c in self.collectors:
            try:
                c.emit_success(tries, elapsed, target_name)
            except Exception:
                pass

    def emit_failure(self, tries: int, elapsed: float, target_name: str, exception_type: str) -> None:
        for c in self.collectors:
            try:
                c.emit_failure(tries, elapsed, target_name, exception_type)
            except Exception:
                pass

    def emit_circuit_breaker_open(self, breaker_name: str) -> None:
        for c in self.collectors:
            try:
                c.emit_circuit_breaker_open(breaker_name)
            except Exception:
                pass

    def emit_circuit_breaker_close(self, breaker_name: str) -> None:
        for c in self.collectors:
            try:
                c.emit_circuit_breaker_close(breaker_name)
            except Exception:
                pass

    def emit_hedge_request(self, target_name: str, hedge_count: int) -> None:
        for c in self.collectors:
            try:
                c.emit_hedge_request(target_name, hedge_count)
            except Exception:
                pass

def setup_backon_observability():
    """Initializes backon metrics with Prometheus and OpenTelemetry."""
    collectors = []
    try:
        from backon import PrometheusMetrics, OTelMetrics, set_metrics_collector

        # Try to set up Prometheus
        try:
            collectors.append(PrometheusMetrics())
            logger.info("Backon Prometheus metrics initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Backon Prometheus metrics: {e}")

        # Try to set up OpenTelemetry
        try:
            collectors.append(OTelMetrics(meter_name="pipecatapp.backon"))
            logger.info("Backon OpenTelemetry metrics initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Backon OpenTelemetry metrics: {e}")

        if collectors:
            if len(collectors) == 1:
                set_metrics_collector(collectors[0])
            else:
                set_metrics_collector(MultiMetricsCollector(collectors))
            logger.info(f"Backon observability enabled with {len(collectors)} collectors")

    except ImportError as e:
        logger.warning(f"Backon observability dependencies missing: {e}")

# Default setup
setup_backon_observability()
