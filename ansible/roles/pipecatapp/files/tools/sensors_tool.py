import logging
import random

class SensorsTool:
    """A tool for interacting with the ship's sensors."""

    def scan_area(self) -> str:
        """Scans the area for intruder activity."""
        logging.info("SENSORS: Scanning area.")
        # In a real implementation, this would return actual sensor data.
        # For now, we'll return a random plausible observation.
        possible_observations = [
            "No intruders detected in the immediate vicinity.",
            "Life signs detected in the engine room. They appear to be examining the core.",
            "A single intruder is standing motionless in the corridor.",
            "Multiple heat signatures detected near the bridge.",
            "Energy fluctuations detected. It could be their equipment."
        ]
        observation = random.choice(possible_observations)
        logging.info(f"SENSORS: Observation: {observation}")
        return observation
