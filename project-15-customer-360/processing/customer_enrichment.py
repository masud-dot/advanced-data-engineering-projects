import pandas as pd


class CustomerEnricher:
    """Builds enriched customer-level attributes for Customer 360."""

    def build_activity_metrics(
        self,
        activity: pd.DataFrame,
    ) -> pd.DataFrame:
        if activity.empty:
            return pd.DataFrame(columns=["customer_id"])

        df = activity.copy()

        result = (
            df.groupby("customer_id", as_index=False)
            .agg(
                activity_count=("activity_id", "nunique"),
                last_activity_date=("activity_date", "max"),
            )
        )

        activity_counts = (
            pd.crosstab(
                df["customer_id"],
                df["activity_type"],
            )
            .reset_index()
        )

        rename_map = {
            "login": "login_count",
            "product_view": "product_view_count",
            "support_ticket": "support_ticket_count",
            "email_open": "email_open_count",
            "purchase": "activity_purchase_count",
        }

        activity_counts = activity_counts.rename(columns=rename_map)

        result = result.merge(
            activity_counts,
            on="customer_id",
            how="left",
        )

        metric_columns = [
            "login_count",
            "product_view_count",
            "support_ticket_count",
            "email_open_count",
            "activity_purchase_count",
        ]

        for column in metric_columns:
            if column not in result.columns:
                result[column] = 0
            result[column] = result[column].fillna(0).astype(int)

        return result

    def build_preferred_category(
        self,
        transactions: pd.DataFrame,
    ) -> pd.DataFrame:
        if transactions.empty or "category" not in transactions.columns:
            return pd.DataFrame(columns=["customer_id", "preferred_category"])

        category_revenue = (
            transactions.groupby(
                ["customer_id", "category"],
                as_index=False,
            )["revenue"]
            .sum()
            .sort_values(
                ["customer_id", "revenue"],
                ascending=[True, False],
            )
        )

        preferred = (
            category_revenue
            .drop_duplicates(subset=["customer_id"])
            [["customer_id", "category"]]
            .rename(columns={"category": "preferred_category"})
        )

        return preferred.reset_index(drop=True)

    def enrich(
        self,
        customers: pd.DataFrame,
        transaction_metrics: pd.DataFrame,
        activity_metrics: pd.DataFrame,
        preferred_category: pd.DataFrame,
    ) -> pd.DataFrame:
        profile = customers.copy()

        profile = profile.merge(
            transaction_metrics,
            on="customer_id",
            how="left",
        )

        profile = profile.merge(
            activity_metrics,
            on="customer_id",
            how="left",
        )

        profile = profile.merge(
            preferred_category,
            on="customer_id",
            how="left",
        )

        numeric_columns = [
            "order_count",
            "total_revenue",
            "total_units",
            "average_order_value",
            "activity_count",
            "login_count",
            "product_view_count",
            "support_ticket_count",
            "email_open_count",
            "activity_purchase_count",
        ]

        for column in numeric_columns:
            if column in profile.columns:
                profile[column] = profile[column].fillna(0)

        integer_columns = [
            "order_count",
            "total_units",
            "activity_count",
            "login_count",
            "product_view_count",
            "support_ticket_count",
            "email_open_count",
            "activity_purchase_count",
        ]

        for column in integer_columns:
            if column in profile.columns:
                profile[column] = profile[column].astype(int)

        if "total_revenue" in profile.columns:
            profile["total_revenue"] = profile["total_revenue"].round(2)

        if "average_order_value" in profile.columns:
            profile["average_order_value"] = (
                profile["average_order_value"].round(2)
            )

        return profile.reset_index(drop=True)
