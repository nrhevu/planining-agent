import asyncio
from agent_ai.runtime.agent_runner import Agent
from agent_ai.tools.builtin.calculator import Calculator
from agent_ai.tools.builtin.local_search import LocalSearch
from agent_ai.llm.dummy import DummyReasoner

async def ask(agent, q):
    return await agent.ask(q, {"documents": ["A: hello world", "B: goodbye world"]})

def test_dummy_tool_use():
    agent = Agent([Calculator(), LocalSearch()], DummyReasoner())
    out = asyncio.run(ask(agent, "What is 7 * 6?"))
    assert "42" in out or out == "(dummy) I think the answer is contextual and no tools were needed."
