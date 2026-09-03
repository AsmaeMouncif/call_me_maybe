# __main__.py
import sys

from llm_sdk import Small_LLM_Model

from .errors import CallMeMaybeError
from .function_name import extract_function_name, generate_function_name
from .json_loader import load_json_file, parse_models
from .models import FunctionCallResult, FunctionDefinition, PromptEntry
from .output_writer import write_results


def parse_args() -> tuple[str, str, str]:
    """Parse --functions_definition/--input/--output flags with sane defaults."""
    functions_definition = "data/input/functions_definition.json"
    input_file = "data/input/function_calling_tests.json"
    output = "data/output/function_calling_results.json"
    known_flags = ["--functions_definition", "--input", "--output"]
    for i, arg in enumerate(sys.argv):
        if arg not in known_flags:
            continue
        if i + 1 >= len(sys.argv):
            raise ValueError(f"Missing value for argument: {arg}")
        if arg == "--functions_definition":
            functions_definition = sys.argv[i + 1]
        elif arg == "--input":
            input_file = sys.argv[i + 1]
        elif arg == "--output":
            output = sys.argv[i + 1]
    return functions_definition, input_file, output


def main() -> None:
    """Load inputs, generate a function call per prompt, and write the results file."""
    try:
        functions_definition, input_file, output = parse_args()

        raw_functions = load_json_file(functions_definition)
        raw_prompts = load_json_file(input_file)
        functions = parse_models(raw_functions, FunctionDefinition, functions_definition)
        prompts = parse_models(raw_prompts, PromptEntry, input_file)

        model = Small_LLM_Model()

        results: list[FunctionCallResult] = []
        for entry in prompts:
            raw_name = generate_function_name(model, entry.prompt, functions)
            name = extract_function_name(raw_name)
            results.append(
                FunctionCallResult(
                    prompt=entry.prompt,
                    name=name,
                    parameters={},  # TODO next: real argument extraction
                )
            )

        write_results(results, output)

    except CallMeMaybeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
