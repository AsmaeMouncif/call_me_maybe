

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
