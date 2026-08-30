import json
import sys
from pathlib import Path
from .models import FunctionCallResult


def write_results(results: list[FunctionCallResult], output_path: str) -> None:
    path = Path(output_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Could not create output directory for {path}: {e}", file=sys.stderr)
        sys.exit(1)
    data = []
    for result in results:
        data.append(result.model_dump())
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"Could not write output file {path}: {e}", file=sys.stderr)
        sys.exit(1)
