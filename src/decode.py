from collections.abc import Iterable
import numpy as np


def pick_from_ids(logits: list[float], allowed: Iterable[int]) -> int:
    candidates = np.fromiter(allowed, dtype=np.int64)
    