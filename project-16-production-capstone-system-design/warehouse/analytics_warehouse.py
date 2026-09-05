from pathlib import Path
import pandas as pd


class LocalRedshiftWarehouse:
    """
    Local analytics warehouse equivalent.

    Production mapping: Amazon Redshift.
    Local implementation: Parquet-backed analytical tables.
    """

    def __init__(self, root: str = "local_warehouse"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def load(self, table_name: str, df: pd.DataFrame) -> Path:
        path = self.root / f"{table_name}.parquet"
        df.to_parquet(path, index=False)
        return path

    def read(self, table_name: str) -> pd.DataFrame:
        return pd.read_parquet(self.root / f"{table_name}.parquet")
