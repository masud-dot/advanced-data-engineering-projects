import pandas as pd

from performance.memory import optimize_dataframe_memory


def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    result = optimize_dataframe_memory(df)

    for column in result.select_dtypes(
        include=["object"]
    ).columns:
        result[column] = result[column].fillna("UNKNOWN")

    return result
