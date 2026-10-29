import logging
from duckduckgo_search import DDGS
from typing import List, Dict, Any, Optional
import json

class KeylessWebResearcherTool:
    """A tool for performing keyless web search using DuckDuckGo.

    This provides a fallback web research mechanism when primary APIs are
    unavailable or rate-limited.
    """

    def __init__(self):
        self.name = "keyless_web_researcher"
        self.description = "Perform keyless web searches using DuckDuckGo."
        self.logger = logging.getLogger(__name__)

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "keyless_web_researcher"),
                "description": getattr(self, "description", "Tool KeylessWebResearcherTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["search_text", "search_news"],
                            "description": "The type of search to perform."
                        },
                        "query": {
                            "type": "string",
                            "description": "The search query."
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default 5)."
                        }
                    },
                    "required": ["action", "query"]
                }
            }
        }

    def execute(self, action: str, query: str, max_results: int = 5, **kwargs) -> str:
        """Executes the requested DuckDuckGo search action."""
        try:
            if action == "search_text":
                return self.search_text(query, max_results)
            elif action == "search_news":
                return self.search_news(query, max_results)
            else:
                return f"Error: Unknown action '{action}'"
        except Exception as e:
            self.logger.error(f"DuckDuckGo search error: {e}")
            return f"Error performing search: {e}"

    def search_text(self, query: str, max_results: int = 5) -> str:
        """Performs a text search using DuckDuckGo."""
        results = []
        try:
            with DDGS() as ddgs:
                # Use text() generator to fetch results
                for r in ddgs.text(query, max_results=max_results):
                    results.append(r)

            if not results:
                return f"No results found for query: {query}"

            return json.dumps(results, indent=2)

        except Exception as e:
            self.logger.error(f"DuckDuckGo text search failed: {e}")
            return f"Search failed: {e}"

    def search_news(self, query: str, max_results: int = 5) -> str:
        """Performs a news search using DuckDuckGo."""
        results = []
        try:
            with DDGS() as ddgs:
                # Use news() generator to fetch news results
                for r in ddgs.news(query, max_results=max_results):
                    results.append(r)

            if not results:
                return f"No news found for query: {query}"

            return json.dumps(results, indent=2)

        except Exception as e:
            self.logger.error(f"DuckDuckGo news search failed: {e}")
            return f"News search failed: {e}"
