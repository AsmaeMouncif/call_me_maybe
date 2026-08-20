import sys


def parse_args() -> tuple[str, str, str]:
    functions_definition = "data/input/functions_definition.json"
    input_file = "data/input/function_calling_tests.json"
    output_file = "data/output/function_calls.json"
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
            output_file = sys.argv[i + 1]
    return functions_definition, input_file, output_file


def main() -> None:
    functions_definition, input_file, output_file = parse_args()
    print(functions_definition)
    print(input_file)
    print(output_file)


if __name__ == "__main__":
    main()
