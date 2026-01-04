import time
import threading

class ExpertTracker:
    """A thread-safe class to track performance and health metrics for LLM experts.

    This class maintains a record for each expert, tracking its type, health,
    and performance metrics like latency and success/failure rates. This data
    is used by the coordinator LLM to make intelligent routing decisions.

    Attributes:
        experts (dict): A dictionary to store the state of each expert.
        lock (threading.Lock): A lock to ensure thread-safe updates to the experts dict.
    """
    def __init__(self):
        """Initializes the ExpertTracker."""
        self.experts = {}
        self.lock = threading.Lock()

    def register_expert(self, name: str, expert_type: str):
        """Registers a new expert to be tracked.

        Args:
            name (str): The unique name of the expert.
            expert_type (str): The type of the expert ('local' or 'external').
        """
        with self.lock:
            if name not in self.experts:
                self.experts[name] = {
                    "type": expert_type,
                    "health": "unknown",
                    "success_count": 0,
                    "failure_count": 0,
                    "total_latency": 0.0,
                    "average_latency": 0.0,
                    "last_seen": 0,
                }

    def record_success(self, name: str, latency: float):
        """Records a successful interaction with an expert.

        Args:
            name (str): The name of the expert.
            latency (float): The duration of the successful call in seconds.
        """
        with self.lock:
            if name in self.experts:
                expert = self.experts[name]
                expert["health"] = "healthy"
                expert["success_count"] += 1
                expert["total_latency"] += latency
                expert["average_latency"] = expert["total_latency"] / expert["success_count"]
                expert["last_seen"] = time.time()

    def record_failure(self, name: str):
        """Records a failed interaction with an expert.

        Args:
            name (str): The name of the expert.
        """
        with self.lock:
            if name in self.experts:
                expert = self.experts[name]
                expert["health"] = "unhealthy"
                expert["failure_count"] += 1
                expert["last_seen"] = time.time()

    def get_metrics_for_prompt(self) -> str:
        """Generates a string of all expert metrics formatted for an LLM prompt.

        Returns:
            str: A formatted string detailing the status and performance of each expert.
        """
        with self.lock:
            if not self.experts:
                return "No expert performance data available."

            metrics_string = "You have the following experts available, with their current performance metrics:\n"
            for name, data in sorted(self.experts.items()):
                metrics_string += (
                    f"- Expert: {name} (Type: {data['type']}, Health: {data['health']})\n"
                    f"  - Successes: {data['success_count']}, Failures: {data['failure_count']}\n"
                    f"  - Average Latency: {data['average_latency']:.2f}s\n"
                )
            return metrics_string