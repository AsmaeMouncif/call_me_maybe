import json
import sys
from llm_sdk import Small_LLM_Model


def load_vocab(model: Small_LLM_Model) -> dict[str, int]:
    path = model.get_path_to_vocab_file()
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except (FileNotFoundError, IsADirectoryError, PermissionError) as e:
        print(f"Could not read vocab file {path}: {e}", file=sys.stderr)
        sys.exit(1)
    try:
        vocab = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in vocab file {path}: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(vocab, dict):
        print(
            f"Unexpected vocab format in {path}: expected an object",
            file=sys.stderr,
        )
        sys.exit(1)
    return vocab


def build_reverse_vocab(vocab: dict[str, int]) -> dict[int, str]:
    return {v: k for k, v in vocab.items()}

def bytes_to_unicode() -> dict[int, str]:
    Printable