# function_name.py
import json
from llm_sdk import Small_LLM_Model
from .errors import GenerationError
from .models import FunctionDefinition
from .prompt import build_prompt


def get_function_names(functions: list[FunctionDefinition]) -> list[str]:
    """Return the list of callable function names."""
    return [function.name for function in functions]


def build_function_candidate(model: Small_LLM_Model, function_name: str) -> list[int]:
    """Tokenize the full JSON snippet for one candidate function name."""
    text = '{"name": "' + function_name + '"}'
    return model.encode(text).squeeze(0).tolist()


def build_function_candidates(
    model: Small_LLM_Model, function_names: list[str]
) -> list[list[int]]:
    """Tokenize every candidate function name snippet."""
    return [build_function_candidate(model, name) for name in function_names]


def get_valid_next_tokens(
    candidates: list[list[int]], generated_ids: list[int]
) -> set[int]:
    """Return the set of tokens that keep generated_ids a valid prefix of some candidate."""
    valid_token_ids: set[int] = set()
    prefix_length = len(generated_ids)
    for candidate in candidates:
        if candidate[:prefix_length] == generated_ids and prefix_length < len(candidate):
            valid_token_ids.add(candidate[prefix_length])
    return valid_token_ids


def select_next_token(logits: list[float], valid_tokens: set[int]) -> int:
    """Pick the highest-logit token among the allowed ones (constrained decoding)."""
    return max(valid_tokens, key=lambda token_id: logits[token_id])


def generate_function_name(
    model: Small_LLM_Model,
    prompt: str,
    functions: list[FunctionDefinition],
) -> str:
    """Generate the '{"name": "..."}' snippet, constrained to a known function name."""
    input_ids = model.encode(build_prompt(functions, prompt)).squeeze(0).tolist()
    candidates = build_function_candidates(model, get_function_names(functions))

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


def extract_function_name(raw_snippet: str) -> str:
    """Parse the '{"name": "..."}' snippet produced by generate_function_name."""
    try:
        data = json.loads(raw_snippet)
        return str(data["name"])
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise GenerationError(
            f"Could not extract function name from generated output: {raw_snippet!r}"
        ) from exc
