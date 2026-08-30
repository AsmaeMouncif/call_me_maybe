from .models import FunctionDefinition


def get_function_names(
    functions: list[FunctionDefinition],
) -> list[str]:
    function_names = []
    for function in functions:
        function_names.append(function.name)
    return function_names
