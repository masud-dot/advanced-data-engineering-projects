import pandas as pd


class AnalyticsWarehouse:
    """Builds warehouse-style fact and dimension datasets."""

    def build_customer_dimension(self, customers: pd.DataFrame) -> pd.DataFrame:
        columns = [
            column
            for column in [
                "customer_id",
                "customer_name",
                "email",
                "region",
            ]
            if column in customers.columns
        ]

        dimension = customers[columns].copy()

        if "customer_id" in dimension.columns:
            dimension = dimension.drop_duplicates(subset=["customer_id"])

        return dimension.reset_index(drop=True)

    def build_product_dimension(self, products: pd.DataFrame) -> pd.DataFrame:
        columns = [
            column
            for column in [
                "product_id",
                "product_name",
                "category",
                "price",
            ]
            if column in products.columns
        ]

        dimension = products[columns].copy()

        if "product_id" in dimension.columns:
            dimension = dimension.drop_duplicates(subset=["product_id"])

        return dimension.reset_index(drop=True)

    def build_fact_orders(self, orders: pd.DataFrame) -> pd.DataFrame:
        columns = [
            column
            for column in [
                "order_id",
                "customer_id",
                "product_id",
                "order_date",
                "quantity",
                "amount",
                "revenue",
                "region",
                "category",
            ]
            if column in orders.columns
        ]

        fact = orders[columns].copy()

        if "order_id" in fact.columns:
            fact = fact.drop_duplicates(subset=["order_id"])

        return fact.reset_index(drop=True)

    def daily_sales(self, fact_orders: pd.DataFrame) -> pd.DataFrame:
        if "order_date" not in fact_orders.columns:
            return pd.DataFrame()

        revenue_column = (
            "revenue"
            if "revenue" in fact_orders.columns
            else "amount"
            if "amount" in fact_orders.columns
            else None
        )

        if revenue_column is None:
            return pd.DataFrame()

        df = fact_orders.copy()
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

        group_columns = ["order_date"]

        if "region" in df.columns:
            group_columns.append("region")

        result = (
            df.dropna(subset=["order_date"])
            .groupby(group_columns, as_index=False)
            .agg(
                revenue=(revenue_column, "sum"),
                order_count=("order_id", "nunique"),
            )
        )

        result["average_order_value"] = (
            result["revenue"] / result["order_count"]
        )

        return result.sort_values(
            ["order_date", "revenue"],
            ascending=[False, False],
        ).reset_index(drop=True)

    def product_performance(self, fact_orders: pd.DataFrame) -> pd.DataFrame:
        if "product_id" not in fact_orders.columns:
            return pd.DataFrame()

        revenue_column = (
            "revenue"
            if "revenue" in fact_orders.columns
            else "amount"
            if "amount" in fact_orders.columns
            else None
        )

        if revenue_column is None:
            return pd.DataFrame()

        aggregations = {
            "order_count": ("order_id", "nunique"),
            "revenue": (revenue_column, "sum"),
        }

        if "quantity" in fact_orders.columns:
            aggregations["units_sold"] = ("quantity", "sum")

        result = fact_orders.groupby(
            "product_id",
            as_index=False,
        ).agg(**aggregations)

        return result.sort_values(
            "revenue",
            ascending=False,
        ).reset_index(drop=True)

    def customer_performance(self, fact_orders: pd.DataFrame) -> pd.DataFrame:
        if "customer_id" not in fact_orders.columns:
            return pd.DataFrame()

        revenue_column = (
            "revenue"
            if "revenue" in fact_orders.columns
            else "amount"
            if "amount" in fact_orders.columns
            else None
        )

        if revenue_column is None:
            return pd.DataFrame()

        result = (
            fact_orders.groupby("customer_id", as_index=False)
            .agg(
                order_count=("order_id", "nunique"),
                total_revenue=(revenue_column, "sum"),
            )
        )

        result["average_order_value"] = (
            result["total_revenue"] / result["order_count"]
        )

        return result.sort_values(
            "total_revenue",
            ascending=False,
        ).reset_index(drop=True)

    def build_all(self, datasets: dict) -> dict:
        fact_orders = self.build_fact_orders(datasets["orders"])

        return {
            "fact_orders": fact_orders,
            "dim_customer": self.build_customer_dimension(
                datasets["customers"]
            ),
            "dim_product": self.build_product_dimension(
                datasets["products"]
            ),
            "daily_sales": self.daily_sales(fact_orders),
            "product_performance": self.product_performance(fact_orders),
            "customer_performance": self.customer_performance(fact_orders),
        }
