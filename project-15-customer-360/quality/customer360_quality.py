import pandas as pd


class Customer360Quality:
    """Validates Customer 360 datasets and calculates quality scores."""

    def validate_profile(self, profile: pd.DataFrame) -> dict:
        checks = {}

        required_columns = [
            "customer_id",
            "customer_name",
            "email",
            "region",
            "signup_date",
            "order_count",
            "lifetime_value",
            "activity_count",
        ]

        missing_columns = [
            column for column in required_columns
            if column not in profile.columns
        ]

        checks["required_columns"] = {
            "passed": not missing_columns,
            "missing": missing_columns,
        }

        checks["customer_id_not_null"] = {
            "passed": (
                "customer_id" in profile.columns
                and profile["customer_id"].notna().all()
            )
        }

        checks["customer_id_unique"] = {
            "passed": (
                "customer_id" in profile.columns
                and profile["customer_id"].is_unique
            )
        }

        checks["revenue_non_negative"] = {
            "passed": (
                "lifetime_value" in profile.columns
                and (profile["lifetime_value"] >= 0).all()
            )
        }

        checks["orders_non_negative"] = {
            "passed": (
                "order_count" in profile.columns
                and (profile["order_count"] >= 0).all()
            )
        }

        checks["profile_not_empty"] = {
            "passed": not profile.empty
        }

        passed = sum(
            1 for check in checks.values()
            if check["passed"]
        )

        total = len(checks)
        score = round((passed / total) * 100, 2) if total else 0.0

        return {
            "score": score,
            "status": "PASS" if score >= 95 else "FAIL",
            "checks": checks,
        }

    def validate_referential_integrity(
        self,
        customers: pd.DataFrame,
        transactions: pd.DataFrame,
    ) -> dict:
        if customers.empty:
            return {
                "passed": False,
                "invalid_customer_ids": 0,
            }

        customer_ids = set(customers["customer_id"].dropna())

        invalid = (
            ~transactions["customer_id"].isin(customer_ids)
        ).sum()

        return {
            "passed": bool(invalid == 0),
            "invalid_customer_ids": int(invalid),
        }

    def validate(
        self,
        profile: pd.DataFrame,
        customers: pd.DataFrame | None = None,
        transactions: pd.DataFrame | None = None,
    ) -> dict:
        profile_result = self.validate_profile(profile)

        result = {
            "profile_quality": profile_result,
        }

        if customers is not None and transactions is not None:
            result["referential_integrity"] = (
                self.validate_referential_integrity(
                    customers,
                    transactions,
                )
            )

        return result
