from .models import FunctionDefinition


SELECT_INSTRUCTION = (
    "Choose the one function that answers the request. JSON only."
)
ARGUMENT_INSTRUCTION = (
    "Extract this function's arguments from the request. JSON only."
)
THINK_BLOCK = ""


def describe_function(function: FunctionDefinition) -> str:
    signature = ", ".join(
        f"{name}: {spec.type}" for name, spec in function.parameters.items()
    )
    return f"- {function.name}({signature}): {function.description}"


def _wrap(system: str, request: str) -> str:
    return (
        f"<|im_start|>system\n{system}<|im_end|>\n"
        f"<|im_start|>user\n{request}<|im_end|>\n"
        f"<|im_start|>assistant\n{THINK_BLOCK}"
    )
