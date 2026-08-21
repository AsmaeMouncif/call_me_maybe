import json
import sys
from typing import Any


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
        print(f"Empty JSON file: {path}", file=sys.stder)
        sys.exit(1)
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)
