from pathlib import Path
import pandas as pd


class LocalDataLake:
    """Local filesystem equivalent of S3 Bronze/Silver/Gold storage."""

    def __init__(self, root: str = "production_lake"):
        self.root = Path(root)

    def write(self, df: pd.DataFrame, layer: str, table: str) -> Path:
        path = self.root / layer
        path.mkdir(parents=True, exist_ok=True)

        output = path / f"{table}.parquet"
        df.to_parquet(output, index=False)

        return output

    def read(self, layer: str, table: str) -> pd.DataFrame:
        path = self.root / layer / f"{table}.parquet"
        return pd.read_parquet(path)
