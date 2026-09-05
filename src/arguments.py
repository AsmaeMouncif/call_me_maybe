from llm_sdk import Small_LLM_Model
from .models import FunctionDefinition
from .prompt import build_argument_prompt


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


def get_next_number_state(state: str, token_id: int, is_last_parameter: bool = False) -> str:
    if state == "start":
        if token_id == 12 or token_id in get_number_digit_tokens():
            return "digits"
    if state == "digits":
        if token_id in get_number_digit_tokens():
            return "digits"
        if token_id == 13:
            return "decimal"
        if token_id in get_number_end_tokens(is_last_parameter):
            return "finished"
    if state == "decimal":
        if token_id in get_number_digit_tokens():
            return "decimal"
        if token_id in get_number_end_tokens(is_last_parameter):
            return "finished"
    return "invalid"


def get_parameter_decoder(parameter_type: str) -> str:
    if parameter_type == "number":
        return "number"
    if parameter_type == "string":
        return "string"
    raise ValueError(
        f"Unsupported parameter type: {parameter_type}"
    )


def generate_number(model: Small_LLM_Model, input_ids: list[int], is_last_parameter: bool) -> list[int]:
    generated_ids: list[int] = []
    state = "start"
    while True:
        if state == "start":
            valid_tokens = get_number_start_tokens()
        elif state == "digits":
            valid_tokens = get_number_digit_tokens() | get_decimal_point_tokens() | get_number_end_tokens(is_last_parameter)
        elif state == "decimal":
            valid_tokens = get_number_digit_tokens() | get_number_end_tokens(is_last_parameter)
        else:
            raise ValueError(
                f"Invalid number state: {state}"
            )
        logits = model.get_logits_from_input_ids(input_ids)
        next_token = max(valid_tokens, key=lambda token_id: logits[token_id])
        end_tokens =  get_number_end_tokens(is_last_parameter)
        if (
            state in {"digits", "decimal"}
            and next_token in end_tokens
        ):
            break
        generated_ids.append(next_token)
        input_ids.append(next_token)
        state = get_next_number_state(state, next_token, is_last_parameter)
    return generated_ids


def generate_arguments(model: Small_LLM_Model, function: FunctionDefinition, request: str) -> str:
    input_ids = model.encode(build_argument_prompt(function, request)).squeeze(0).tolist()
    generated_ids: list[int] = []
    parameters = list(function.parameters.items())
    for index, (parameter_name, parameter_spec) in enumerate(parameters):
        is_first = index == 0
        is_last = index == len(parameters) - 1
        if is_first:
            prefix = '{"' + parameter_name + '": '
        else:
            prefix = ', "' + parameter_name + '": '
        prefix_ids = model.encode(prefix).squeeze(0).tolist()
        generated_ids.extend(prefix_ids)
        input_ids.extend(prefix_ids)
        decoder_type = get_parameter_decoder(parameter_spec.type)
        if decoder_type == "number":
            number_ids = generate_number(model, input_ids, is_last_parameter=is_last)
            generated_ids.extend(number_ids)
        if decoder_type == "string":
    if parameters:
        closing_ids = model.encode("}").squeeze(0).tolist()
        generated_ids.extend(closing_ids)
    return model.decode(generated_ids)
