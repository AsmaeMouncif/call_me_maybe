


SELECT_INSTRUCTION = (
    "Choose the one function that answers the request. JSON only."
)
ARGUMENT_INSTRUCTION = (
    "Extract this function's arguments from the request. JSON only."
)


def _wrap(system: str, request: str) -> str:
    return (
        f"<|im_start|>user
Hi there!<|im_end|>"
    )