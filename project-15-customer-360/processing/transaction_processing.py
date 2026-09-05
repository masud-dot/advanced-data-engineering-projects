import pandas as pd


class TransactionProcessor:
    """Processes customer transactions for Customer 360 analytics."""

    def process(
        self,
        orders: pd.DataFrame,
        products: pd.DataFrame,
    ) -> pd.DataFrame:
        df = orders.copy()

        product_columns = [
            column
            for column in ["product_id", "product_name", "category", "price"]
            if column in products.columns
        ]

        if product_columns:
            df = df.merge(
                products[product_columns],
                on="product_id",
                how="left",
                suffixes=("", "_product"),
            )

        if "quantity" in df.columns and "price" in df.columns:
            df["calculated_revenue"] = df["quantity"] * df["price"]

        if "amount" in df.columns:
            df["revenue"] = pd.to_numeric(
                df["amount"], errors="coerce"
            )
        elif "calculated_revenue" in df.columns:
            df["revenue"] = df["calculated_revenue"]

        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(
                df["order_date"], errors="coerce"
            )

        if "revenue" in df.columns:
            df["revenue"] = pd.to_numeric(
                df["revenue"], errors="coerce"
            )

        if "quantity" in df.columns:
            df["quantity"] = pd.to_numeric(
                df["quantity"], errors="coerce"
            )

        df["transaction_month"] = (
            df["order_date"].dt.to_period("M").astype("string")
        )

        return df.reset_index(drop=True)

    def customer_transaction_metrics(
        self,
        transactions: pd.DataFrame,
    ) -> pd.DataFrame:
        if transactions.empty:
            return pd.DataFrame()

        result = (
            transactions.groupby("customer_id", as_index=False)
            .agg(
                order_count=("order_id", "nunique"),
                total_revenue=("revenue", "sum"),
                total_units=("quantity", "sum"),
                first_order_date=("order_date", "min"),
                last_order_date=("order_date", "max"),
            )
        )

        result["average_order_value"] = (
            result["total_revenue"] / result["order_count"]
        )

        return result
