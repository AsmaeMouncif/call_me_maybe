from llm_sdk import Small_LLM_Model
from .models import FunctionDefinition


def get_function_names(functions: list[FunctionDefinition]) -> list[str]:
    names = []
    for function in functions:
        names.append(function.name)
    return names


def build_function_candidate(model: Small_LLM_Model, function_name: str) -> list[int]:
    text = '{"name": "' + function_name + '"}'
    return model.encode(text).squeeze(0).tolist()


def build_function_candidates(model: Small_LLM_Model, function_names: list[str]) -> list[list[int]]:
    candidates = []
    for function_name in function_names:
        candidate = build_function_candidate(model, function_name)
        candidates.append(candidate)
    return candidates
