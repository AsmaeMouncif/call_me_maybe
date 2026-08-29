from pathlib import Path
from .models import FunctionCallResult


def write_results(results: list[FunctionCallResult], output_path: str) -> None:
    path = Path(output_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Could not create output directory for {path}: {e}", file=sys.stderr)
        sys.exit(1)

    try:
    
    except OSError as e:
        print(f"Could not create output directory for {path}: {e}", file=sys.stderr)
        sys.exit(1)