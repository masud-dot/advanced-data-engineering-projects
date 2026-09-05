import pandas as pd


def memory_usage_mb(df: pd.DataFrame) -> float:
    return float(df.memory_usage(deep=True).sum() / (1024 ** 2))


def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    optimized = df.copy()

    for column in optimized.columns:
        dtype = optimized[column].dtype

        if pd.api.types.is_integer_dtype(dtype):
            optimized[column] = pd.to_numeric(
                optimized[column],
                downcast="integer",
            )

        elif pd.api.types.is_float_dtype(dtype):
            optimized[column] = pd.to_numeric(
                optimized[column],
                downcast="float",
            )

        elif pd.api.types.is_object_dtype(dtype):
            unique_ratio = optimized[column].nunique(
                dropna=False
            ) / max(len(optimized), 1)

            if unique_ratio < 0.5:
                optimized[column] = optimized[column].astype("category")

    return optimized
