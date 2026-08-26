import json
from llm_sdk import Small_LLM_Model


def load_model() -> Small_LLM_Model:
    return Small_LLM_Model()


def load_vocab(model: Small_LLM_Model) -> dict[str, int]:
    path = model.get_path_to_vocab_file()
    with open(path, encoding="utf-8") as f:
        vocab: dict[str, int] = json.load(f)
    return vocab


def build_reverse_vocab(vocab: dict[str, int]) -> dict[int, str]:
    return {v: k for k, v in vocab.items()}
