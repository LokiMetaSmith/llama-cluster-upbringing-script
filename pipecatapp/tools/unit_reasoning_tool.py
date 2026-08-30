import logging
from typing import Dict, Any, Union

class UnitReasoningTool:
    """
    A tool for converting physical measurements, units, and color palettes
    without domain-specific hardcoding.
    """

    def __init__(self):
        self.name = "unit_reasoning"
        self.description = (
            "Perform measurement unit conversions (length, mass, temperature, data) "
            "and palette color reasoning for agents."
        )
        self.logger = logging.getLogger(__name__)

        self.conversions = {
            "meters_to_feet": lambda m: m * 3.28084,
            "feet_to_meters": lambda ft: ft / 3.28084,
            "kg_to_lbs": lambda kg: kg * 2.20462,
            "lbs_to_kg": lambda lbs: lbs / 2.20462,
            "celsius_to_fahrenheit": lambda c: (c * 9/5) + 32,
            "fahrenheit_to_celsius": lambda f: (f - 32) * 5/9,
            "bytes_to_mb": lambda b: b / (1024 * 1024),
            "mb_to_bytes": lambda mb: mb * 1024 * 1024
        }

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "conversion_type": {
                            "type": "string",
                            "enum": list(self.conversions.keys()),
                            "description": "The specific conversion transformation to apply."
                        },
                        "value": {
                            "type": "number",
                            "description": "The numeric value to convert."
                        }
                    },
                    "required": ["conversion_type", "value"]
                }
            }
        }

    def execute(self, conversion_type: str, value: Union[int, float], **kwargs) -> str:
        if conversion_type not in self.conversions:
            return f"Error: Unknown conversion type '{conversion_type}'. Supported: {', '.join(self.conversions.keys())}"

        try:
            converted = self.conversions[conversion_type](float(value))
            return f"Result: {round(converted, 4)} ({conversion_type})"
        except Exception as e:
            self.logger.error(f"Error performing unit conversion: {e}")
            return f"Error performing conversion: {e}"
