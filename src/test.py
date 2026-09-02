from llm_sdk import Small_LLM_Model

from .json_loader import load_json_file, parse_models
from .models import FunctionDefinition
from .prompt import build_prompt


def main() -> None:
    model = Small_LLM_Model()

    functions_data = load_json_file(
        "data/input/functions_definition.json"
    )

    functions = parse_models(
        functions_data,
        FunctionDefinition,
        "data/input/functions_definition.json",
    )

    request = "What is the sum of 2 and 3?"

    prompt = build_prompt(
        functions,
        request,
    )

    input_ids = model.encode(prompt).squeeze(0).tolist()

    generated_ids = []

    for _ in range(50):
        logits = model.get_logits_from_input_ids(input_ids)

        next_token_id = max(
            range(len(logits)),
            key=lambda i: logits[i],
        )

        input_ids.append(next_token_id)
        generated_ids.append(next_token_id)

    response = model.decode(generated_ids)

    print("Generated response:")
    print(response)


if __name__ == "__main__":
    main()
