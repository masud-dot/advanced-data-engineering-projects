from pathlib import Path

import pandas as pd


class CustomerIngestion:
    """Loads source datasets for the Customer 360 platform."""

    REQUIRED_FILES = {
        "customers": "customers.csv",
        "orders": "orders.csv",
        "products": "products.csv",
        "activity": "customer_activity.csv",
    }

    def __init__(self, source_dir="sample_data"):
        self.source_dir = Path(source_dir)

    def _load_csv(self, filename):
        path = self.source_dir / filename

        if not path.exists():
            raise FileNotFoundError(f"Source file not found: {path}")

        return pd.read_csv(path)

    def load_customers(self):
        return self._load_csv(self.REQUIRED_FILES["customers"])

    def load_orders(self):
        return self._load_csv(self.REQUIRED_FILES["orders"])

    def load_products(self):
        return self._load_csv(self.REQUIRED_FILES["products"])

    def load_activity(self):
        return self._load_csv(self.REQUIRED_FILES["activity"])

    def load_all(self):
        return {
            "customers": self.load_customers(),
            "orders": self.load_orders(),
            "products": self.load_products(),
            "activity": self.load_activity(),
        }

    def row_counts(self, datasets):
        return {
            name: len(dataframe)
            for name, dataframe in datasets.items()
        }
