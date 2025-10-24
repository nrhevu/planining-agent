from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

@dataclass
class Message:
    role: Role
    content: str
    name: Optional[str] = None  # for tool messages
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ToolCall:
    tool_name: str
    arguments: Dict[str, Any]

@dataclass
class ToolResult:
    tool_name: str
    result: Any
    ok: bool = True
    error_message: Optional[str] = None
