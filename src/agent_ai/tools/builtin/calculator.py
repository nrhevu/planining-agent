from __future__ import annotations
import ast, operator as op
from typing import Any, Dict
from pydantic import BaseModel
from agent_ai.tools.base import Tool, ToolInput, ToolOutput

_ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg}

def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Num):
        return float(node.n)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ops:
        return _ops[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _ops:
        return _ops[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError("Unsupported expression")

class CalcIn(ToolInput):
    expression: str

class CalcOut(ToolOutput):
    result: float

class Calculator(Tool):
    def __init__(self):
        super().__init__("calculator", "Evaluate a math expression, e.g., '2 + 2 * 3'", CalcIn, CalcOut)

    async def __call__(self, args: Dict[str, Any], ctx: Dict[str, Any]) -> CalcOut:
        data = self.InputModel(**args)
        try:
            node = ast.parse(data.expression, mode="eval").body
            val = _eval(node)
            return self.OutputModel(result=val)
        except Exception as e:
            raise RuntimeError(f"calc error: {e}")
