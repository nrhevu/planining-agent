from __future__ import annotations
from typing import Dict, Any
from agent_ai.core.state import AgentState
from agent_ai.tools.registry import ToolRegistry
from agent_ai.tools.builtin.calculator import Calculator
from agent_ai.tools.builtin.local_search import LocalSearch
from agent_ai.tools.builtin.web_search_stub import WebSearchStub
from agent_ai.llm.dummy import DummyReasoner
from agent_ai.reasoning.react import react_loop

class Agent:
    def __init__(self, tools: list = None, lm=None):
        self.registry = ToolRegistry()
        for t in (tools or []):
            self.registry.register(t)
        self.lm = lm or DummyReasoner()

    async def ask(self, query: str, ctx: Dict[str, Any] | None = None) -> str:
        state = AgentState()
        return await react_loop(state, self.registry, self.lm, query, ctx)

async def default_agent_answer(query: str) -> str:
    agent = Agent(tools=[Calculator(), LocalSearch(), WebSearchStub()])
    ctx = {"documents": [
        "The Eiffel Tower is in Paris and was completed in 1889.",
        "Python 3.10 introduced pattern matching with PEP 634.",
        "Bangkok is the capital of Thailand.",
    ]}
    return await agent.ask(query, ctx)
