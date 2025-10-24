from __future__ import annotations
from typing import Any, Dict, List, Tuple
from pydantic import BaseModel
from difflib import get_close_matches
from agent_ai.tools.base import Tool, ToolInput, ToolOutput

class LocalSearchIn(ToolInput):
    query: str
    top_k: int = 5

class LocalSearchOut(ToolOutput):
    matches: List[Tuple[str, float]]  # (text, score)

class LocalSearch(Tool):
    def __init__(self):
        super().__init__("local_search", "Search in-memory documents loaded in context under ctx['documents'].", LocalSearchIn, LocalSearchOut)

    async def __call__(self, args: Dict[str, Any], ctx: Dict[str, Any]) -> LocalSearchOut:
        data = self.InputModel(**args)
        docs: List[str] = ctx.get("documents", [])
        candidates = get_close_matches(data.query, docs, n=data.top_k, cutoff=0.0)
        out = [(c, 1.0 - abs(len(c) - len(data.query)) / max(len(c), 1)) for c in candidates]
        return self.OutputModel(matches=out)
