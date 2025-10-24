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
