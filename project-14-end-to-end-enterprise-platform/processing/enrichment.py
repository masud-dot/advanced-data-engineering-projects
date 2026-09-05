import pandas as pd


class DataEnricher:
    """Enriches transformed datasets with customer and product attributes."""

    def enrich_orders(
        self,
        orders: pd.DataFrame,
        customers: pd.DataFrame,
        products: pd.DataFrame,
    ) -> pd.DataFrame:
        df = orders.copy()

        customer_columns = [
            column
            for column in ["customer_id", "customer_name", "email", "region"]
            if column in customers.columns
        ]

        if customer_columns:
            df = df.merge(
                customers[customer_columns],
                on="customer_id",
                how="left",
                suffixes=("", "_customer"),
            )

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
            df["revenue"] = df["amount"]
        elif "calculated_revenue" in df.columns:
            df["revenue"] = df["calculated_revenue"]

        if "order_date" in df.columns:
            df["order_year"] = df["order_date"].dt.year
            df["order_month"] = df["order_date"].dt.month
            df["order_day"] = df["order_date"].dt.day

        return df

    def enrich_all(self, datasets: dict) -> dict:
        enriched_orders = self.enrich_orders(
            datasets["orders"],
            datasets["customers"],
            datasets["products"],
        )

        return {
            "customers": datasets["customers"],
            "products": datasets["products"],
            "orders": enriched_orders,
        }
