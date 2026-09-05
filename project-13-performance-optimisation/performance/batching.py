from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


def process_in_batches(
    data: list[T],
    batch_size: int,
    processor: Callable[[list[T]], R],
) -> list[R]:
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero")

    results = []

    for start in range(0, len(data), batch_size):
        batch = data[start:start + batch_size]
        results.append(processor(batch))

    return results


def chunk_dataframe(df, batch_size: int):
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero")

    for start in range(0, len(df), batch_size):
        yield df.iloc[start:start + batch_size]
