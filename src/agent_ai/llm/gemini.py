from __future__ import annotations
import os
from typing import Any, Dict, List
from google import generativeai as genai
from agent_ai.core.messages import Message, Role
from .base import LanguageModel

JSON_HINT = (
    'You are a tool-using agent. Return ONLY JSON with either '
    '{"type":"tool","tool_name":"...","tool_input":{...}} or '
    '{"type":"final","answer":"..."}. '
    'Do not include any extra commentary.'
)

class GeminiReasoner(LanguageModel):
    def __init__(self, api_key: str | None = None, model_name: str = "gemini-1.5-flash", temperature: float = 0.2, max_output_tokens: int = 1024):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is required. Set env var or pass api_key=...")
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        genai.configure(api_key=self.api_key)
        self._model = genai.GenerativeModel(model_name=self.model_name)

    def _to_contents(self, messages: List[Message], tools_schema: Dict[str, Any] | None) -> List[dict]:
        contents: List[dict] = []
        tool_desc = f"Available tools: {list(tools_schema.keys())}" if tools_schema else "No tools available."
        priming = f"{JSON_HINT}\n{tool_desc}"
        contents.append({"role": "user", "parts": [{"text": priming}]})

        for m in messages:
            if m.role == Role.USER:
                contents.append({"role": "user", "parts": [{"text": m.content}]})
            elif m.role == Role.ASSISTANT:
                contents.append({"role": "model", "parts": [{"text": m.content}]})
            elif m.role == Role.TOOL:
                name = m.name or "tool"
                contents.append({
                    "role": "user",
                    "parts": [{"text": f"TOOL[{name}] RESULT:\n{m.content}"}]
                })
        return contents

    async def generate(self, messages: List[Message], tools_schema: Dict[str, Any] | None = None) -> str:
        contents = self._to_contents(messages, tools_schema)
        config = {
            "temperature": self.temperature,
            "candidate_count": 1,
            "max_output_tokens": self.max_output_tokens,
        }
        try:
            resp = self._model.generate_content(contents=contents, generation_config=config)
            return getattr(resp, "text", str(resp))
        except Exception as e:
            return f'{{"type":"final","answer":"Gemini error: {str(e).replace("\"","'")}"}}'
