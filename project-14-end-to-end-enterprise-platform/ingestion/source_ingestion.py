from pathlib import Path
import pandas as pd


class SourceIngestion:
    """Loads source datasets for the enterprise data platform."""

    def __init__(self, source_dir="sample_data"):
        self.source_dir = Path(source_dir)

    def _load_csv(self, filename):
        path = self.source_dir / filename

        if not path.exists():
            raise FileNotFoundError(f"Source file not found: {path}")

        return pd.read_csv(path)

    def load_customers(self):
        return self._load_csv("customers.csv")

    def load_products(self):
        return self._load_csv("products.csv")

    def load_orders(self):
        return self._load_csv("orders.csv")

    def load_all(self):
        return {
            "customers": self.load_customers(),
            "products": self.load_products(),
            "orders": self.load_orders(),
        }
