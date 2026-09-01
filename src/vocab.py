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


def bytes_to_unicode() -> dict[int, str]:
    printable: list[int] = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    mapped: list[int] = printable[:]
    shift = 0
    for byte in range(256):
        if byte not in printable:
            printable.append(byte)
            mapped.append(256 + shift)
            shift += 1
    return {byte: chr(code) for byte, code in zip(printable, mapped)}


def decode_token(token: str, byte_decoder: dict[str, int]) -> str:
    pass

