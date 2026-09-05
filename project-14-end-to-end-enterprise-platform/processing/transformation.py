import pandas as pd


class DataTransformer:
    """Transforms raw source data into clean Silver-layer datasets."""

    def transform_customers(self, customers: pd.DataFrame) -> pd.DataFrame:
        df = customers.copy()

        df.columns = [column.strip().lower() for column in df.columns]

        if "customer_id" in df.columns:
            df["customer_id"] = pd.to_numeric(
                df["customer_id"], errors="coerce"
            ).astype("Int64")

        if "customer_name" in df.columns:
            df["customer_name"] = df["customer_name"].astype("string").str.strip()

        if "email" in df.columns:
            df["email"] = df["email"].astype("string").str.strip().str.lower()

        return df.drop_duplicates(subset=["customer_id"])

    def transform_products(self, products: pd.DataFrame) -> pd.DataFrame:
        df = products.copy()

        df.columns = [column.strip().lower() for column in df.columns]

        if "product_id" in df.columns:
            df["product_id"] = pd.to_numeric(
                df["product_id"], errors="coerce"
            ).astype("Int64")

        if "product_name" in df.columns:
            df["product_name"] = df["product_name"].astype("string").str.strip()

        if "price" in df.columns:
            df["price"] = pd.to_numeric(df["price"], errors="coerce")

        return df.drop_duplicates(subset=["product_id"])

    def transform_orders(self, orders: pd.DataFrame) -> pd.DataFrame:
        df = orders.copy()

        df.columns = [column.strip().lower() for column in df.columns]

        if "order_id" in df.columns:
            df["order_id"] = pd.to_numeric(
                df["order_id"], errors="coerce"
            ).astype("Int64")

        if "customer_id" in df.columns:
            df["customer_id"] = pd.to_numeric(
                df["customer_id"], errors="coerce"
            ).astype("Int64")

        if "product_id" in df.columns:
            df["product_id"] = pd.to_numeric(
                df["product_id"], errors="coerce"
            ).astype("Int64")

        if "quantity" in df.columns:
            df["quantity"] = pd.to_numeric(
                df["quantity"], errors="coerce"
            )

        if "amount" in df.columns:
            df["amount"] = pd.to_numeric(
                df["amount"], errors="coerce"
            )

        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(
                df["order_date"], errors="coerce"
            )

        required_columns = [
            column
            for column in ["order_id", "customer_id", "product_id", "order_date"]
            if column in df.columns
        ]

        if required_columns:
            df = df.dropna(subset=required_columns)

        if "amount" in df.columns:
            df = df[df["amount"] >= 0]

        return df.drop_duplicates(subset=["order_id"])

    def transform_all(self, datasets: dict) -> dict:
        return {
            "customers": self.transform_customers(datasets["customers"]),
            "products": self.transform_products(datasets["products"]),
            "orders": self.transform_orders(datasets["orders"]),
        }
