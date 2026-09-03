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


def get_valid_next_tokens(candidates: list[list[int]], generated_ids: list[int]) -> set[int]:
    valid_token_ids: set[int] = set()
    for candidate in candidates:
        prefix_length = len(generated_ids)
        if candidate[:prefix_length] == generated_ids:
            if prefix_length < len(candidate):
                valid_token_ids.add(candidate[prefix_length])
    return valid_token_ids


def select_next_token(logits: list[float], valid_tokens: set[int]) -> int:
    return max(valid_tokens, key=lambda token_id: logits[token_id])


def generate_function_name(model: Small_LLM_Model, prompt: str, functions: list[FunctionDefinition]) -> str:
    input_ids = model.encode(build_prompt(functions, prompt)).squeeze(0).tolist()
    function_names = get_function_names(functions)
    candidates = build_function_candidates(model, functions)
    generated_ids: list[int] = []
    while True:
        valid_tokens = get_valid_next_tokens(candidates, generated_ids)
        if not valid_tokens:
            break
        logits = model.get_logits_from_input_ids(input_ids)
        next_token = select_next_token(logits, valid_tokens)
        generated_ids.append(next_token)
        input_ids.append(next_token)
        if generated_ids in candidates:
            break
    return model.decode(generated_ids)
