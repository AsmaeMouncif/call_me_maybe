from collections.abc import Iterable
import numpy as np
from .errors import GenerationError


def pick_from_ids(logits: list[float], allowed: Iterable[int]) -> int:
    candidates = np.fromiter(allowed, dtype=np.int64)

candidates.size
raise GenerationError("No token is available at this step")