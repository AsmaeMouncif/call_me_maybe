from pydantic import BaseModel


class ParameterSpec(BaseModel):
    type: str


class ReturnSpec(BaseModel):
    type: str


class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParameterSpec]
    returns: ReturnSpec


class Prompt(BaseModel):
    prompt: str


class Fun(BaseModel):
    prompt: str
    name: str
    parameters: dict[str, Any]
