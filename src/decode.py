from collections.abc import Iterable


def pick_from_ids(logits: list[float], allowed: Iterable[int]) -> int:


candidates = np.fromiter(allowed,dtype=int)