import pandas as pd


class CustomerSegmentation:
    """Segments customers using transparent business rules."""

    def segment(self, profile: pd.DataFrame) -> pd.DataFrame:
        result = profile.copy()

        if result.empty:
            result["customer_segment"] = pd.Series(dtype="string")
            return result

        result["customer_segment"] = result.apply(
            self._segment_customer,
            axis=1,
        )

        return result

    @staticmethod
    def _segment_customer(row) -> str:
        revenue = float(row.get("lifetime_value", 0))
        orders = int(row.get("order_count", 0))
        engagement = int(row.get("engagement_score", 0))
        recency = int(row.get("recency_days", -1))
        customer_age = int(row.get("customer_age_days", 0))

        if orders == 0:
            return "PROSPECT"

        if revenue >= 2000 and engagement >= 8:
            return "VIP"

        if recency >= 30:
            return "AT_RISK"

        if customer_age <= 90:
            return "NEW_CUSTOMER"

        if orders >= 3 and revenue >= 1000:
            return "LOYAL"

        if engagement >= 8:
            return "ENGAGED"

        return "ACTIVE"

    def segment_summary(self, profile: pd.DataFrame) -> pd.DataFrame:
        if profile.empty or "customer_segment" not in profile.columns:
            return pd.DataFrame()

        summary = (
            profile.groupby("customer_segment", as_index=False)
            .agg(
                customer_count=("customer_id", "nunique"),
                total_revenue=("lifetime_value", "sum"),
                average_revenue=("lifetime_value", "mean"),
                average_orders=("order_count", "mean"),
                average_engagement=("engagement_score", "mean"),
            )
        )

        summary["total_revenue"] = summary["total_revenue"].round(2)
        summary["average_revenue"] = summary["average_revenue"].round(2)
        summary["average_orders"] = summary["average_orders"].round(2)
        summary["average_engagement"] = summary["average_engagement"].round(2)

        return summary.sort_values(
            "total_revenue",
            ascending=False,
        ).reset_index(drop=True)
