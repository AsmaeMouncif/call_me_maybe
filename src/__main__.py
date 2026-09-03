from .json_loader import load_json_file, parse_models
from .models import FunctionDefinition, PromptEntry
from .vocab import load_vocab, build_reverse_vocab
from .output_writer import write_results
from llm_sdk import Small_LLM_Model
import sys


def parse_args() -> tuple[str, str, str]:
    functions_definition = "data/input/functions_definition.json"
    input_file = "data/input/function_calling_tests.json"
    output = "function_calling_results.json"
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
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    raw_functions = load_json_file(functions_definition)
    raw_prompts = load_json_file(input_file)
    functions = parse_models(
        raw_functions, FunctionDefinition, functions_definition
    )
    prompts = parse_models(
        raw_prompts, PromptEntry, input_file
    )
    model = Small_LLM_Model()
    vocab = load_vocab(model)
    reverse_vocab = build_reverse_vocab(vocab)
    results = []
    write_results(results, output)


if __name__ == "__main__":
    main()
