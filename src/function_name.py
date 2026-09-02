from llm_sdk import Small_LLM_Model
from .models import FunctionDefinition


def get_function_names(functions: list[FunctionDefinition]) -> list[str]:
    names = []
    for function in functions:
        names.append(function.name)
    return names


def build_funcion_candidate(model: Small_LLM_Model, function_name: str) -> list[int]:
    text = '{"name": "' + function_name + '"}'
    return model.decode(text).squeeze(0).tolist()
