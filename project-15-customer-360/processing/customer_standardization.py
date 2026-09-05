import pandas as pd


class CustomerStandardizer:
    """Standardizes Customer 360 source datasets."""

    @staticmethod
    def _normalize_columns(df):
        result = df.copy()
        result.columns = [
            column.strip().lower().replace(" ", "_")
            for column in result.columns
        ]
        return result

    def standardize_customers(self, customers: pd.DataFrame) -> pd.DataFrame:
        df = self._normalize_columns(customers)

        if "customer_id" in df.columns:
            df["customer_id"] = pd.to_numeric(
                df["customer_id"], errors="coerce"
            ).astype("Int64")

        if "customer_name" in df.columns:
            df["customer_name"] = (
                df["customer_name"].astype("string").str.strip()
            )

        if "email" in df.columns:
            df["email"] = (
                df["email"].astype("string").str.strip().str.lower()
            )

        if "region" in df.columns:
            df["region"] = (
                df["region"].astype("string").str.strip().str.title()
            )

        if "signup_date" in df.columns:
            df["signup_date"] = pd.to_datetime(
                df["signup_date"], errors="coerce"
            )

        df = df.dropna(subset=["customer_id"])
        return df.drop_duplicates(subset=["customer_id"]).reset_index(drop=True)

    def standardize_products(self, products: pd.DataFrame) -> pd.DataFrame:
        df = self._normalize_columns(products)

        if "product_id" in df.columns:
            df["product_id"] = pd.to_numeric(
                df["product_id"], errors="coerce"
            ).astype("Int64")

        if "product_name" in df.columns:
            df["product_name"] = (
                df["product_name"].astype("string").str.strip()
            )

        if "category" in df.columns:
            df["category"] = (
                df["category"].astype("string").str.strip().str.title()
            )

        if "price" in df.columns:
            df["price"] = pd.to_numeric(df["price"], errors="coerce")

        df = df.dropna(subset=["product_id"])
        df = df[df["price"].fillna(0) >= 0]
        return df.drop_duplicates(subset=["product_id"]).reset_index(drop=True)

    def standardize_orders(self, orders: pd.DataFrame) -> pd.DataFrame:
        df = self._normalize_columns(orders)

        for column in ["order_id", "customer_id", "product_id"]:
            if column in df.columns:
                df[column] = pd.to_numeric(
                    df[column], errors="coerce"
                ).astype("Int64")

        for column in ["quantity", "amount"]:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors="coerce")

        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(
                df["order_date"], errors="coerce"
            )

        required = [
            column
            for column in [
                "order_id",
                "customer_id",
                "product_id",
                "order_date",
            ]
            if column in df.columns
        ]

        if required:
            df = df.dropna(subset=required)

        if "quantity" in df.columns:
            df = df[df["quantity"] > 0]

        if "amount" in df.columns:
            df = df[df["amount"] >= 0]

        return df.drop_duplicates(
            subset=["order_id"]
        ).reset_index(drop=True)

    def standardize_activity(
        self, activity: pd.DataFrame
    ) -> pd.DataFrame:
        df = self._normalize_columns(activity)

        if "activity_id" in df.columns:
            df["activity_id"] = pd.to_numeric(
                df["activity_id"], errors="coerce"
            ).astype("Int64")

        if "customer_id" in df.columns:
            df["customer_id"] = pd.to_numeric(
                df["customer_id"], errors="coerce"
            ).astype("Int64")

        for column in ["activity_type", "channel"]:
            if column in df.columns:
                df[column] = (
                    df[column].astype("string").str.strip().str.lower()
                )

        if "activity_date" in df.columns:
            df["activity_date"] = pd.to_datetime(
                df["activity_date"], errors="coerce"
            )

        required = [
            column
            for column in ["activity_id", "customer_id", "activity_date"]
            if column in df.columns
        ]

        if required:
            df = df.dropna(subset=required)

        return df.drop_duplicates(
            subset=["activity_id"]
        ).reset_index(drop=True)

    def standardize_all(self, datasets: dict) -> dict:
        return {
            "customers": self.standardize_customers(datasets["customers"]),
            "products": self.standardize_products(datasets["products"]),
            "orders": self.standardize_orders(datasets["orders"]),
            "activity": self.standardize_activity(datasets["activity"]),
        }
