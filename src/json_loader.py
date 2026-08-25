import json
import sys
from typing import Any, Type, TypeVar
from pydantic import BaseModel, ValidationError


def load_json_file(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except IsADirectoryError:
        print(f"Path is a directory, not a file: {path}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Permission denied: {path}", file=sys.stderr)
        sys.exit(1)
    if not content.strip():
        print(f"Empty JSON file: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)


T = TypeVar("T", bound=BaseModel)


def parse_models(raw_data: Any, model: Type[T], source: str) -> list[T]:
    if not isinstance(raw_data, list):
        print(f"Excepted a JSON array in {source}", file=sys.stderr)
        sys.exit(1)
    result: list[T] = []
    try:
        for item in raw_data:
            parsed_item = model(**item)
            result.append(parsed_item)
    except ValidationError as e:
        print(f"Validation error in {source}: {e}", file=sys.stderr)
        sys.exit(1)
    except TypeError as e:
        print(f"Invalid item structure in {source}: {e}", file=sys.stderr)
        sys.exit(1)
    return result
