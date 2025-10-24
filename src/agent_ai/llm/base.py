from __future__ import annotations
from typing import Any, Dict, List, Protocol
from agent_ai.core.messages import Message

class LanguageModel(Protocol):
    async def generate(self, messages: List[Message], tools_schema: Dict[str, Any] | None = None) -> str:
        """Return assistant text. If tools_schema is provided, the model should output a JSON plan
        with either {"type":"tool", "tool_name":"...", "tool_input":{...}} or {"type":"final", "answer":"..."}.
        """
        ...
