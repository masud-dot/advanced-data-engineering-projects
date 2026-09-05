import pytest

from performance.parallel import parallel_map


def test_parallel_map():
    result = parallel_map(
        [1, 2, 3, 4],
        lambda value: value * 2,
        workers=2,
    )

    assert result == [2, 4, 6, 8]


def test_parallel_workers_must_be_positive():
    with pytest.raises(ValueError):
        parallel_map(
            [1, 2],
            lambda value: value,
            workers=0,
        )
