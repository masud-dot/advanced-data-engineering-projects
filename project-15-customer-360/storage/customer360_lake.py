from pathlib import Path

import pandas as pd


class Customer360Lake:
    """Manages Bronze, Silver, and Gold Customer 360 datasets."""

    def __init__(self, root="customer360_lake"):
        self.root = Path(root)
        self.bronze = self.root / "bronze"
        self.silver = self.root / "silver"
        self.gold = self.root / "gold"

        for path in [self.bronze, self.silver, self.gold]:
            path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _write(df: pd.DataFrame, layer: Path, name: str):
        path = layer / f"{name}.parquet"
        df.to_parquet(path, index=False)
        return path

    @staticmethod
    def _read(layer: Path, name: str):
        path = layer / f"{name}.parquet"

        if not path.exists():
            raise FileNotFoundError(
                f"Customer 360 dataset not found: {path}"
            )

        return pd.read_parquet(path)

    def write_bronze(self, datasets: dict):
        return {
            name: self._write(df, self.bronze, name)
            for name, df in datasets.items()
        }

    def write_silver(self, datasets: dict):
        return {
            name: self._write(df, self.silver, name)
            for name, df in datasets.items()
        }

    def write_gold(self, datasets: dict):
        return {
            name: self._write(df, self.gold, name)
            for name, df in datasets.items()
        }

    def read_bronze(self, name: str):
        return self._read(self.bronze, name)

    def read_silver(self, name: str):
        return self._read(self.silver, name)

    def read_gold(self, name: str):
        return self._read(self.gold, name)
