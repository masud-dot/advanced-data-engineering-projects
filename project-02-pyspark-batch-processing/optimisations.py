from pyspark.sql import DataFrame
from pyspark.sql.functions import broadcast


def optimise_with_broadcast(
    large_df: DataFrame,
    small_lookup_df: DataFrame,
    join_column: str,
) -> DataFrame:
    """
    Demonstrate a broadcast join for a genuinely small lookup DataFrame.

    The lookup DataFrame is broadcast to executors to avoid a large
    shuffle when the lookup table is small enough to fit in executor
    memory.
    """
    if join_column not in large_df.columns:
        raise ValueError(
            f"Join column '{join_column}' is missing from large_df."
        )

    if join_column not in small_lookup_df.columns:
        raise ValueError(
            f"Join column '{join_column}' is missing "
            "from small_lookup_df."
        )

    return large_df.join(
        broadcast(small_lookup_df),
        on=join_column,
        how="left",
    )


def repartition_for_processing(
    df: DataFrame,
    partitions: int = 8,
) -> DataFrame:
    """Repartition a DataFrame for parallel processing."""
    if partitions < 1:
        raise ValueError("partitions must be greater than zero.")

    return df.repartition(partitions)
