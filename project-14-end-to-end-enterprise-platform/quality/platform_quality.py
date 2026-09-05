import pandas as pd


class PlatformQuality:
    """Runs data-quality checks across the enterprise platform."""

    def _check_required_columns(self, df, required_columns):
        missing = [column for column in required_columns if column not in df.columns]
        return {
            "passed": len(missing) == 0,
            "missing_columns": missing,
        }

    def _check_completeness(self, df, columns):
        if not columns:
            return {"passed": True, "null_count": 0}

        existing = [column for column in columns if column in df.columns]
        null_count = int(df[existing].isna().sum().sum())

        return {
            "passed": null_count == 0,
            "null_count": null_count,
        }

    def _check_duplicates(self, df, key):
        if key not in df.columns:
            return {
                "passed": False,
                "duplicate_count": None,
            }

        duplicate_count = int(df[key].duplicated().sum())

        return {
            "passed": duplicate_count == 0,
            "duplicate_count": duplicate_count,
        }

    def _check_non_negative(self, df, column):
        if column not in df.columns:
            return {
                "passed": True,
                "invalid_count": 0,
            }

        invalid_count = int((df[column] < 0).sum())

        return {
            "passed": invalid_count == 0,
            "invalid_count": invalid_count,
        }

    def _check_references(self, orders, customers, products):
        customer_invalid = 0
        product_invalid = 0

        if "customer_id" in orders.columns and "customer_id" in customers.columns:
            customer_invalid = int(
                (~orders["customer_id"].isin(customers["customer_id"])).sum()
            )

        if "product_id" in orders.columns and "product_id" in products.columns:
            product_invalid = int(
                (~orders["product_id"].isin(products["product_id"])).sum()
            )

        return {
            "passed": customer_invalid == 0 and product_invalid == 0,
            "invalid_customer_references": customer_invalid,
            "invalid_product_references": product_invalid,
        }

    def validate(
        self,
        customers: pd.DataFrame,
        products: pd.DataFrame,
        orders: pd.DataFrame,
    ) -> dict:
        checks = {}

        checks["customers_schema"] = self._check_required_columns(
            customers,
            ["customer_id"],
        )

        checks["products_schema"] = self._check_required_columns(
            products,
            ["product_id"],
        )

        checks["orders_schema"] = self._check_required_columns(
            orders,
            ["order_id", "customer_id", "product_id", "order_date"],
        )

        checks["orders_completeness"] = self._check_completeness(
            orders,
            ["order_id", "customer_id", "product_id", "order_date"],
        )

        checks["order_duplicates"] = self._check_duplicates(
            orders,
            "order_id",
        )

        checks["revenue_validation"] = self._check_non_negative(
            orders,
            "revenue",
        )

        checks["reference_integrity"] = self._check_references(
            orders,
            customers,
            products,
        )

        if "order_date" in orders.columns:
            invalid_dates = int(
                pd.to_datetime(
                    orders["order_date"],
                    errors="coerce",
                ).isna().sum()
            )
        else:
            invalid_dates = 0

        checks["date_validation"] = {
            "passed": invalid_dates == 0,
            "invalid_date_count": invalid_dates,
        }

        passed_checks = sum(
            1 for result in checks.values()
            if result["passed"]
        )

        total_checks = len(checks)

        score = (
            round((passed_checks / total_checks) * 100, 2)
            if total_checks
            else 0.0
        )

        return {
            "score": score,
            "passed": score >= 95,
            "passed_checks": passed_checks,
            "total_checks": total_checks,
            "checks": checks,
        }
