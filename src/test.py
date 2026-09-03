from llm_sdk import Small_LLM_Model

from .function_name import (
    generate_function_name,
)
from .json_loader import load_json_file, parse_models
from .models import FunctionDefinition


def main() -> None:
    model = Small_LLM_Model()

    data = load_json_file(
        "data/input/functions_definition.json"
    )

    functions = parse_models(
        data,
        FunctionDefinition,
        "data/input/functions_definition.json",
    )

    function_names = [
        function.name
        for function in functions
    ]

    prompt = "What is the sum of 2 and 3?"

    result = generate_function_name(
        model,
        prompt,
        functions,
    )

    print("Prompt:")
    print(prompt)

    print("Generated function:")
    print(result)


if __name__ == "__main__":
    main()
