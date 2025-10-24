import asyncio
import typer
from agent_ai.runtime.agent_runner import default_agent_answer

app = typer.Typer()

@app.command()
def ask(q: str):
    """Ask the agent a question."""
    ans = asyncio.run(default_agent_answer(q))
    typer.echo(ans)

if __name__ == "__main__":
    app()
