from .json_loader import load_json_file
import sys


def parse_args() -> tuple[str, str, str]:
    functions_definition = "data/input/functions_definition.json"
    input_file = "data/input/function_calling_tests.json"
    output = "data/output/function_calls.json"
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
    try:
        functions_definition, input_file, output = parse_args()
        functions = load_json_file(functions_definition)
        prompts = load_json_file(input_file)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    print(functions)
    print(prompts)


if __name__ == "__main__":
    main()
