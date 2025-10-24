from __future__ import annotations
from rich.console import Console
from rich.table import Table

_console = Console()

def info(msg: str) -> None:
    _console.log(msg)

def table(title: str, rows: list[tuple[str, str]]) -> None:
    t = Table(title=title)
    t.add_column("Key")
    t.add_column("Value")
    for k, v in rows:
        t.add_row(k, v)
    _console.print(t)
