import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Function calling tool")
    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("functions_definition:", args.functions_definition)
    print("input:", args.input)
    print("output:", args.output)
    Path("data/output").mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()
