from pathlib import Path
import pandas as pd


class LocalIcebergTable:
    """
    Lightweight local abstraction representing an Iceberg table.

    Production mapping:
    S3 + Iceberg table + catalog.

    Local mapping:
    Parquet table with schema-aware writes.
    """

    def __init__(self, root: str = "production_lake"):
        self.root = Path(root)

    def write(self, layer: str, table: str, df: pd.DataFrame) -> Path:
        target = self.root / layer
        target.mkdir(parents=True, exist_ok=True)

        path = target / f"{table}.parquet"
        df.to_parquet(path, index=False)

        return path

    def snapshot(self, layer: str, table: str) -> pd.DataFrame:
        path = self.root / layer / f"{table}.parquet"
        return pd.read_parquet(path)
