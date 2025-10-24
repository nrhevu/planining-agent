# Agent AI Codebase — Search & Reasoning (Python)

A pragmatic, extensible Python codebase for a tool-using agent that can plan, reason, and call tools (e.g., search, calculator) safely. Designed to be small, testable, and easy to grow into production.

## Highlights
- Clear abstractions: LanguageModel, Tool, AgentPolicy (ReAct-style), MemoryStore
- Tool registry with schema-validated inputs/outputs (Pydantic v2)
- Reasoning loop (single/multi-step), with guardrails (token/tool budget, stop conditions)
- Search-ready: includes a local semantic-ish search tool and an optional web search provider shim
- CLI example, tests, typed Python, structured logging

## Repo Layout
See project files for full structure and details.

## Basic User Guide (Gemini)

### 1) Prerequisites

* Python 3.10+
* A Google AI Studio API key (Gemini). Create one at [https://ai.google.dev](https://ai.google.dev)

### 2) Install

```bash
pip install -e .
```

> If you aren't developing locally, you can also install the deps directly:

```bash
pip install google-generativeai pydantic typer httpx rich
```

### 3) Configure

Set your API key and (optionally) model name.

```bash
export GOOGLE_API_KEY="<your-key>"
export AGENT_LLM=gemini              # switches the runtime to GeminiReasoner
export GEMINI_MODEL=gemini-1.5-flash # optional; default is gemini-1.5-flash
```

### 4) Run the CLI

```bash
python examples/search_cli.py "What's 77 * 33?"
python examples/search_cli.py "find facts about Bangkok and Eiffel Tower"
```

The agent will pick tools using the ReAct loop; with `AGENT_LLM=gemini`, responses come from Gemini.

### 5) Programmatic Use

```python
import asyncio
from agent_ai.runtime.agent_runner import Agent
from agent_ai.tools.builtin.calculator import Calculator
from agent_ai.tools.builtin.local_search import LocalSearch
from agent_ai.llm.gemini import GeminiReasoner

async def main():
    agent = Agent(tools=[Calculator(), LocalSearch()], lm=GeminiReasoner())
    ans = await agent.ask("What is 12 * (7 + 5)?", ctx={"documents": ["Bangkok is Thailand's capital."]})
    print(ans)

asyncio.run(main())
```

### 6) Swapping Models

Change `AGENT_LLM` or pass a different `lm=` when constructing `Agent`. For Gemini, set `GEMINI_MODEL` to e.g. `gemini-1.5-pro` for stronger reasoning or `gemini-1.5-flash` for speed.

### 7) Troubleshooting

* **`ValueError: GOOGLE_API_KEY is required`** → export `GOOGLE_API_KEY`.
* **Empty/Non-JSON outputs** → the loop forwards raw text; ensure prompts instruct JSON-only. See `JSON_HINT` in `gemini.py`.
* **429/Quotas** → reduce traffic, add retries/backoff around `generate_content`.

### 8) Next Steps

* Replace `web_search_stub` with a real provider (Tavily/Bing/SerpAPI) and keep the same schema.
* Add a vector-backed `Retrieve` tool for RAG.
* Expose a FastAPI service and secure with API keys.

---

**That’s it!** This gives you a clean backbone to build a capable, Gemini-powered, tool-using agent quickly and safely.

