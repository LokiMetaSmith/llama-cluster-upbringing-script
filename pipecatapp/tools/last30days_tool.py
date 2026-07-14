import os
import requests
import logging
from typing import Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("Last30DaysTool")

class Last30DaysTool:
    """
    Research what people actually say about any topic in the last 30 days.
    Pulls posts and engagement from Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub, and the web.
    """
    name = "last30days"
    description = (
        "Research what people actually say about any topic in the last 30 days. "
        "Pulls posts and engagement from Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub, and the web."
    )
    input_schema = {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The core subject or entity to research (e.g., 'Sam Altman', 'Claude Code vs Cursor')."
            },
            "query_type": {
                "type": "string",
                "description": "Specific framing/type (e.g., 'technical', 'news', 'summary').",
                "enum": ["technical", "news", "summary", "general"]
            },
            "days": {
                "type": "integer",
                "description": "The lookback window in days (default: 30).",
                "default": 30
            },
            "depth": {
                "type": "integer",
                "description": "Defines the scrape depth/breadth (1 = quick, 2 = balanced, 3 = deep).",
                "default": 2,
                "enum": [1, 2, 3]
            }
        },
        "required": ["topic"]
    }

    def __init__(self, service_url: Optional[str] = None, api_key: Optional[str] = None):
        # Allow service_url to be configured dynamically, default to local/Consul DNS address
        self.service_url = service_url or os.getenv("LAST30DAYS_SERVICE_URL", "http://last30days-service.service.consul:8008")
        self.api_key = api_key or os.getenv("TOOL_SERVER_API_KEY")

    def run(self, topic: str, query_type: Optional[str] = None, days: int = 30, depth: int = 2) -> str:
        """
        Runs research on the specified topic.
        """
        url = f"{self.service_url.rstrip('/')}/research"
        payload = {
            "topic": topic,
            "query_type": query_type,
            "days": days,
            "depth": depth
        }

        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        logger.info(f"Forwarding last30days request to {url}")
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=300)
            response.raise_for_status()
            return response.json().get("result", "No results returned from research engine.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to communicate with last30days-service: {e}")
            return f"Error: Failed to communicate with last30days-service: {e}"
