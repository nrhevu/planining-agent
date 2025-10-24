from __future__ import annotations
from typing import Any, Callable, Dict, Optional, Type
from pydantic import BaseModel

class ToolInput(BaseModel):
    pass

class ToolOutput(BaseModel):
    pass

class Tool:
    name: str
    description: str
    InputModel: Type[ToolInput]
    OutputModel: Type[ToolOutput]

    def __init__(self, name: str, description: str, InputModel: Type[ToolInput], OutputModel: Type[ToolOutput]):
        self.name = name
        self.description = description
        self.InputModel = InputModel
        self.OutputModel = OutputModel

    async def __call__(self, args: Dict[str, Any], ctx: Dict[str, Any]) -> ToolOutput:
        raise NotImplementedError

    def json_schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.InputModel.model_json_schema(),
        }
