from llm_sdk import Small_LLM_Model


def get_number_start_tokens() -> set[int]:
    return set(range(15, 25)) | {12}


def get_number_digit_tokens() -> set[int]:
    return set(range(15, 25))


def get_number_end_tokens(is_last_parameter: bool) -> set[int]:
    if is_last_parameter:
        return {92}
    return {11}


def get_decimal_point_tokens() -> set[int]:
    return {13}


def get_number_valid_tokens(state: str, is_last_parameter: bool = False) -> set[int]:
    if state == "start":
        return get_number_start_tokens()
    if state == "digits":
        return (
            get_number_digit_tokens()
            | get_decimal_point_tokens()
            | get_number_end_tokens(is_last_parameter)
        )
    if state == "decimal":
        return (
            get_number_digit_tokens()
            | get_number_end_tokens(is_last_parameter)
        )
    return set()


def encode_fragment(model: Small_LLM_Model, text: str) -> list[int]:
    return model.encode(text).squeeze(0).tolist()

