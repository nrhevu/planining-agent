from __future__ import annotations
from dataclasses import dataclass, field
from typing import Deque, List
from collections import deque
from .messages import Message

@dataclass
class AgentState:
    history: Deque[Message] = field(default_factory=lambda: deque(maxlen=200))
    max_tool_invocations: int = 6
    invocations: int = 0

    def add(self, msg: Message) -> None:
        self.history.append(msg)

    def as_list(self) -> List[Message]:
        return list(self.history)
