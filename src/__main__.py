import sys


def parse_args() -> tuple[str, str, str]:
    functions_definition = "data/input/functions_definition.json"
    input = "data/input/function_calling_tests.json"
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
            input = sys.argv[i + 1]
        elif arg == "--output":
            output = sys.argv[i + 1]
    return functions_definition, input, output


def main() -> None:
    try:
        functions_definition, input, output = parse_args()
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    functions = load_json_file(functions_definition)
    prompts = load_json_file(input)
    print(functions)
    print(prompts)


if __name__ == "__main__":
    main()
