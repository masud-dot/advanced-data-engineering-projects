import pandas as pd


def partition_dataframe(
    df: pd.DataFrame,
    column: str,
) -> dict[str, pd.DataFrame]:
    if column not in df.columns:
        raise KeyError(
            f"Partition column not found: {column}"
        )

    partitions = {}

    for value, partition in df.groupby(
        column,
        dropna=False,
    ):
        key = str(value)
        partitions[key] = partition.copy()

    return partitions
