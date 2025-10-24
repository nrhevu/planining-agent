from __future__ import annotations
import json
from typing import Dict, Any
from agent_ai.core.messages import Message, Role, ToolResult
from agent_ai.core.state import AgentState
from agent_ai.tools.registry import ToolRegistry
from agent_ai.core import logging as log

JSON_HINT = "Return JSON with either {\"type\":\"tool\",\"tool_name\":...,\"tool_input\":{...}} or {\"type\":\"final\",\"answer\":...}."

async def react_loop(state: AgentState, registry: ToolRegistry, lm, user_query: str, ctx: Dict[str, Any] | None = None) -> str:
    ctx = ctx or {}
    state.add(Message(role=Role.USER, content=user_query))

    while state.invocations <= state.max_tool_invocations:
        state.invocations += 1
        # ask the model
        tools_schema = {t.name: t.json_schema() for t in registry.list()}
        raw = await lm.generate(state.as_list(), tools_schema)
        try:
            plan = json.loads(raw)
        except Exception:
            # if the model didn't follow JSON, just return as final text
            return raw

        if plan.get("type") == "final":
            answer = plan.get("answer", "")
            state.add(Message(role=Role.ASSISTANT, content=answer))
            return answer

        if plan.get("type") == "tool":
            tool_name = plan.get("tool_name")
            tool_input = plan.get("tool_input", {})
            try:
                tool = registry.get(tool_name)
            except KeyError:
                state.add(Message(role=Role.ASSISTANT, content=f"Unknown tool: {tool_name}."))
                return f"Unknown tool: {tool_name}"

            try:
                out = await tool(tool_input, ctx)
                result_payload = out.model_dump() if hasattr(out, "model_dump") else dict(out)
                state.add(Message(role=Role.TOOL, name=tool_name, content=json.dumps(result_payload)))
            except Exception as e:
                err = {"error": str(e)}
                state.add(Message(role=Role.TOOL, name=tool_name, content=json.dumps(err)))
                # let the model see the error and decide next step
                continue
        else:
            # unrecognized plan, bail safely
            return "I couldn't produce a valid plan."

    return "Tool budget exhausted; returning without a final answer."