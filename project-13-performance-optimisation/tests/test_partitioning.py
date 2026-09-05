import pandas as pd

from performance.partitioning import partition_dataframe


def test_partition_dataframe():
    df = pd.DataFrame(
        {
            "transaction_date": [
                "2026-09-01",
                "2026-09-01",
                "2026-09-02",
            ],
            "amount": [100.0, 200.0, 300.0],
        }
    )

    partitions = partition_dataframe(
        df,
        "transaction_date",
    )

    assert set(partitions.keys()) == {
        "2026-09-01",
        "2026-09-02",
    }
    assert len(partitions["2026-09-01"]) == 2
    assert len(partitions["2026-09-02"]) == 1
