from concurrent.futures import ThreadPoolExecutor
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


def parallel_map(
    items: list[T],
    func: Callable[[T], R],
    workers: int = 4,
) -> list[R]:
    if workers <= 0:
        raise ValueError("workers must be greater than zero")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(func, items))
