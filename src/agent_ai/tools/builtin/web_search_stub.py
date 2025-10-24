from __future__ import annotations
from typing import Any, Dict, List
from pydantic import BaseModel
from agent_ai.tools.base import Tool, ToolInput, ToolOutput

class WebSearchIn(ToolInput):
    query: str
    top_k: int = 5

class WebSearchOut(ToolOutput):
    results: List[dict]  # {title, url, snippet}

class WebSearchStub(Tool):
    def __init__(self):
        super().__init__(
            "web_search",
            "Stub web search. Replace with real provider (Bing, Google, Tavily, SerpAPI).",
            WebSearchIn,
            WebSearchOut,
        )

    async def __call__(self, args: Dict[str, Any], ctx: Dict[str, Any]) -> WebSearchOut:
        data = self.InputModel(**args)
        return self.OutputModel(results=[{
            "title": f"Result for: {data.query}",
            "url": "https://example.com",
            "snippet": "This is a stubbed search result. Plug in a real provider here.",
        }])
