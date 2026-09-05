import pandas as pd


class ProductionQualityEngine:
    """Data quality checks for the capstone pipeline."""

    def validate_transactions(self, df: pd.DataFrame) -> dict:
        checks = {
            "required_columns": self._required_columns(df),
            "unique_transaction_ids": df["transaction_id"].is_unique,
            "valid_customer_ids": bool(df["customer_id"].notna().all()),
            "valid_amounts": bool((df["amount"] >= 0).all()),
            "valid_timestamps": bool(
                pd.to_datetime(
                    df["transaction_timestamp"], errors="coerce"
                ).notna().all()
            ),
        }

        passed = sum(checks.values())
        score = round((passed / len(checks)) * 100, 2)

        return {
            "score": score,
            "status": "PASS" if score >= 95 else "FAIL",
            "checks": checks,
        }

    @staticmethod
    def _required_columns(df: pd.DataFrame) -> bool:
        required = {
            "transaction_id",
            "customer_id",
            "transaction_timestamp",
            "merchant_category",
            "amount",
            "currency",
            "status",
        }

        return required.issubset(df.columns)
