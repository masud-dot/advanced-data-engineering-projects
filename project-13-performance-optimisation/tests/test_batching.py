import pandas as pd
import pytest

from performance.batching import (
    chunk_dataframe,
    process_in_batches,
)


def test_process_in_batches():
    data = list(range(10))

    result = process_in_batches(
        data,
        batch_size=3,
        processor=sum,
    )

    assert result == [3, 12, 21, 9]


def test_batch_size_must_be_positive():
    with pytest.raises(ValueError):
        process_in_batches(
            [1, 2, 3],
            batch_size=0,
            processor=sum,
        )


def test_chunk_dataframe():
    df = pd.DataFrame({"value": range(10)})

    chunks = list(
        chunk_dataframe(df, batch_size=4)
    )

    assert len(chunks) == 3
    assert len(chunks[0]) == 4
    assert len(chunks[1]) == 4
    assert len(chunks[2]) == 2
