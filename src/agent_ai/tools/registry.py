from __future__ import annotations
from typing import Dict, Iterable, Optional
from .base import Tool

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name}")
        return self._tools[name]

    def list(self) -> Iterable[Tool]:
        return self._tools.values()

    def tools_schema(self) -> dict:
        return {t.name: t.json_schema() for t in self._tools.values()}
