from collections.abc import Iterable
import numpy as np
from .errors import GenerationError


def pick_from_ids(logits: list[float], allowed: Iterable[int]) -> int:
    candidates = np.fromiter(allowed, dtype=np.int64)
    if candidates.size == 0:
        raise GenerationError("No token is available at this step")
    scores = np.asarray(logits, dtype=np.float32)
    candidates = candidates[candidates < scores.size]
    if candidates.size == 0:
        raise GenerationError("Valid tokens full outside the logit vector")
    return int(candidates[int(np.argmax(scores[candidates]))])

