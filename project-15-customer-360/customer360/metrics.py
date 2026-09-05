import pandas as pd


class Customer360Metrics:
    """Calculates business KPIs from Customer 360 profiles."""

    def summary(self, profile: pd.DataFrame) -> dict:
        if profile.empty:
            return {
                "total_customers": 0,
                "total_revenue": 0.0,
                "total_orders": 0,
                "total_units": 0,
                "average_customer_lifetime_value": 0.0,
                "average_order_value": 0.0,
                "average_engagement_score": 0.0,
                "vip_customers": 0,
                "at_risk_customers": 0,
            }

        return {
            "total_customers": int(profile["customer_id"].nunique()),
            "total_revenue": round(
                float(profile["lifetime_value"].sum()), 2
            ),
            "total_orders": int(profile["order_count"].sum()),
            "total_units": int(profile["total_units"].sum()),
            "average_customer_lifetime_value": round(
                float(profile["lifetime_value"].mean()), 2
            ),
            "average_order_value": round(
                float(profile["average_order_value"].replace(
                    [float("inf"), float("-inf")], 0
                ).mean()),
                2,
            ),
            "average_engagement_score": round(
                float(profile["engagement_score"].mean()), 2
            ),
            "vip_customers": int(
                (profile["customer_segment"] == "VIP").sum()
            ),
            "at_risk_customers": int(
                (profile["customer_segment"] == "AT_RISK").sum()
            ),
        }

    def top_customers(
        self,
        profile: pd.DataFrame,
        limit: int = 10,
    ) -> pd.DataFrame:
        if profile.empty:
            return pd.DataFrame()

        columns = [
            column
            for column in [
                "customer_id",
                "customer_name",
                "region",
                "customer_segment",
                "order_count",
                "lifetime_value",
                "average_order_value",
                "engagement_score",
                "preferred_category",
            ]
            if column in profile.columns
        ]

        return (
            profile[columns]
            .sort_values("lifetime_value", ascending=False)
            .head(limit)
            .reset_index(drop=True)
        )

    def segment_counts(self, profile: pd.DataFrame) -> pd.DataFrame:
        if profile.empty or "customer_segment" not in profile.columns:
            return pd.DataFrame()

        return (
            profile.groupby("customer_segment", as_index=False)
            .agg(
                customer_count=("customer_id", "nunique"),
                total_revenue=("lifetime_value", "sum"),
            )
            .sort_values(
                "customer_count",
                ascending=False,
            )
            .reset_index(drop=True)
        )
