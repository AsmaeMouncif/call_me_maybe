from llm_sdk import Small_LLM_Model

from .function_name import build_function_candidate


def main() -> None:
    model = Small_LLM_Model()

    function_name = "fn_add_numbers"

    token_ids = build_function_candidate(
        model,
        function_name,
    )

    print("Function name:")
    print(function_name)

    print("Token IDs:")
    print(token_ids)


if __name__ == "__main__":
    main()