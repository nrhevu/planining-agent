import asyncio
from agent_ai.tools.builtin.calculator import Calculator

async def run(expr: str):
    return (await Calculator()({"expression": expr}, {})).result

def test_calc():
    assert asyncio.run(run("2+2*3")) == 8
    assert round(asyncio.run(run("2**3 + 1")), 3) == 9.0
