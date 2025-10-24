from __future__ import annotations
import json, re
from typing import Any, Dict, List
from agent_ai.core.messages import Message, Role
from .base import LanguageModel

TOOL_PATTERN = re.compile(r"(\d+\s*[+\-*/]\s*\d+)")

class DummyReasoner(LanguageModel):
    async def generate(self, messages: List[Message], tools_schema: Dict[str, Any] | None = None) -> str:
        last_user = next((m for m in reversed(messages) if m.role == Role.USER), None)
        if not last_user:
            return json.dumps({"type": "final", "answer": "No user query."})
        text = last_user.content
        # simple heuristic: if it looks like arithmetic, call calculator
        if TOOL_PATTERN.search(text):
            expr = TOOL_PATTERN.search(text).group(1)
            return json.dumps({"type": "tool", "tool_name": "calculator", "tool_input": {"expression": expr}})
        # else attempt local_search if available
        if "search" in text.lower() or "find" in text.lower():
            return json.dumps({"type": "tool", "tool_name": "local_search", "tool_input": {"query": text, "top_k": 3}})
        return json.dumps({"type": "final", "answer": "(dummy) I think the answer is contextual and no tools were needed."})
