import pandas as pd


class CustomerAnalyticsWarehouse:
    """Provides analytics-ready Customer 360 warehouse views."""

    def build_customer_dimension(
        self,
        customers: pd.DataFrame,
    ) -> pd.DataFrame:
        columns = [
            column
            for column in [
                "customer_id",
                "customer_name",
                "email",
                "region",
                "signup_date",
            ]
            if column in customers.columns
        ]

        return customers[columns].drop_duplicates(
            subset=["customer_id"]
        ).reset_index(drop=True)

    def build_customer_profile(
        self,
        profile: pd.DataFrame,
    ) -> pd.DataFrame:
        return profile.copy().reset_index(drop=True)

    def build_transaction_fact(
        self,
        transactions: pd.DataFrame,
    ) -> pd.DataFrame:
        columns = [
            column
            for column in [
                "order_id",

"customer_id",
                "product_id",
                "product_name",
                "category",
                "quantity",
                "revenue",
                "order_date",
                "transaction_month",
            ]
            if column in transactions.columns
        ]

        return transactions[columns].reset_index(drop=True)

    def revenue_by_region(
        self,
        profile: pd.DataFrame,
    ) -> pd.DataFrame:
        return (
            profile.groupby("region", as_index=False)
            .agg(
                customer_count=("customer_id", "nunique"),
                total_revenue=("lifetime_value", "sum"),
                average_customer_value=("lifetime_value", "mean"),
            )
            .sort_values("total_revenue", ascending=False)
            .reset_index(drop=True)
        )

    def revenue_by_category(
        self,
        transactions: pd.DataFrame,
    ) -> pd.DataFrame:
        if transactions.empty or "category" not in transactions.columns:
            return pd.DataFrame()

        return (
            transactions.groupby("category", as_index=False)
            .agg(
                order_count=("order_id", "nunique"),
                total_revenue=("revenue", "sum"),
                total_units=("quantity", "sum"),
            )
            .sort_values("total_revenue", ascending=False)
            .reset_index(drop=True)
        )

    def segment_performance(
        self,
        profile: pd.DataFrame,
    ) -> pd.DataFrame:
        if profile.empty or "customer_segment" not in profile.columns:
            return pd.DataFrame()

        return (
            profile.groupby("customer_segment", as_index=False)
            .agg(
                customer_count=("customer_id", "nunique"),
                total_revenue=("lifetime_value", "sum"),
                average_revenue=("lifetime_value", "mean"),
                average_orders=("order_count", "mean"),
                average_engagement=("engagement_score", "mean"),
            )
            .sort_values("total_revenue", ascending=False)
            .reset_index(drop=True)
        )
