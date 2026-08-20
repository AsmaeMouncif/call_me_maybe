import sys


def parse_args():
    functions_file = "data/input/functions_definition.json"
    input_file = "data/input/function_calling_tests.json"
    output_file = "data/output/function_calls.json"
    for i, arg in enumerate(sys.argv):
        if arg == "--functions_definition":
            functions_file = sys.argv[i + 1]
        if arg == "--input":
            input_file = sys.argv[i + 1]
        if arg == "--output":
            output_file = sys.argv[i + 1]
    return functions_file, input_file, output_file


def main():
    pass

if __name__ == "__main__":
    main()
