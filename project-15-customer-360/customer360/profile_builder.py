import pandas as pd


class Customer360ProfileBuilder:
    """Builds a unified Customer 360 profile."""

    def build(self, enriched_customers: pd.DataFrame) -> pd.DataFrame:
        profile = enriched_customers.copy()

        if profile.empty:
            return profile

        if "last_order_date" in profile.columns:
            profile["last_order_date"] = pd.to_datetime(
                profile["last_order_date"], errors="coerce"
            )

        if "last_activity_date" in profile.columns:
            profile["last_activity_date"] = pd.to_datetime(
                profile["last_activity_date"], errors="coerce"
            )

        reference_date = self._get_reference_date(profile)

        if "last_order_date" in profile.columns:
            profile["recency_days"] = (
                reference_date - profile["last_order_date"]
            ).dt.days
            profile["recency_days"] = profile["recency_days"].fillna(-1).astype(int)
        else:
            profile["recency_days"] = -1

        if "order_count" in profile.columns:
            profile["purchase_frequency"] = (
                profile["order_count"] / profile["customer_age_days"].clip(lower=1)
            ).round(4) if "customer_age_days" in profile.columns else (
                profile["order_count"].astype(float)
            )

        if "signup_date" in profile.columns:
            profile["customer_age_days"] = (
                reference_date - profile["signup_date"]
            ).dt.days.clip(lower=1)
        else:
            profile["customer_age_days"] = 1

        if "order_count" in profile.columns:
            profile["purchase_frequency"] = (
                profile["order_count"] / profile["customer_age_days"]
            ).round(4)

        profile["lifetime_value"] = (
            profile["total_revenue"]
            if "total_revenue" in profile.columns
            else 0
        )

        profile["engagement_score"] = self._calculate_engagement_score(profile)

        profile["customer_status"] = profile.apply(
            self._customer_status,
            axis=1,
        )

        profile["profile_completeness"] = self._profile_completeness(profile)

        return profile.reset_index(drop=True)

    @staticmethod
    def _get_reference_date(profile: pd.DataFrame) -> pd.Timestamp:
        dates = []

        for column in ["last_order_date", "last_activity_date", "signup_date"]:
            if column in profile.columns:
                values = pd.to_datetime(
                    profile[column], errors="coerce"
                ).dropna()
                if not values.empty:
                    dates.append(values.max())

        return max(dates) if dates else pd.Timestamp.utcnow().tz_localize(None)

    @staticmethod
    def _calculate_engagement_score(profile: pd.DataFrame) -> pd.Series:
        login = profile.get(
            "login_count",
            pd.Series(0, index=profile.index),
        )
        product_views = profile.get(
            "product_view_count",
            pd.Series(0, index=profile.index),
        )
        email_opens = profile.get(
            "email_open_count",
            pd.Series(0, index=profile.index),
        )
        support_tickets = profile.get(
            "support_ticket_count",
            pd.Series(0, index=profile.index),
        )

        score = (
            login * 2
            + product_views * 3
            + email_opens * 2
            - support_tickets
        )

        return score.clip(lower=0).astype(int)

    @staticmethod
    def _customer_status(row) -> str:
        revenue = float(row.get("lifetime_value", 0))
        orders = int(row.get("order_count", 0))
        engagement = int(row.get("engagement_score", 0))
        recency = int(row.get("recency_days", -1))

        if orders == 0:
            return "PROSPECT"

        if revenue >= 2000 and engagement >= 8:
            return "VIP"

        if recency >= 30:
            return "AT_RISK"

        if engagement >= 8:
            return "ENGAGED"

        return "ACTIVE"

    @staticmethod
    def _profile_completeness(profile: pd.DataFrame) -> pd.Series:
        important_columns = [
            "customer_id",
            "customer_name",
            "email",
            "region",
            "signup_date",
            "order_count",
            "total_revenue",
            "last_order_date",
            "activity_count",
        ]

        existing = [
            column for column in important_columns
            if column in profile.columns
        ]

        if not existing:
            return pd.Series(0.0, index=profile.index)

        completeness = (
            profile[existing].notna().sum(axis=1) / len(existing) * 100
        )

        return completeness.round(2)
