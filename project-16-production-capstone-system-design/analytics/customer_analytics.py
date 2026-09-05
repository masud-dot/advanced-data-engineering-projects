import pandas as pd


class CustomerAnalytics:
    def build_customer_summary(self, transactions: pd.DataFrame) -> pd.DataFrame:
        summary = (
            transactions.groupby(
                [
                    "customer_id",
                    "customer_name",
                    "country",
                    "customer_segment",
                ],
                as_index=False,
            )
            .agg(
                transaction_count=("transaction_id", "count"),
                total_amount=("amount", "sum"),
                average_transaction=("amount", "mean"),
            )
        )

        summary["total_amount"] = summary["total_amount"].round(2)
        summary["average_transaction"] = summary["average_transaction"].round(2)

        return summary.sort_values(
            "total_amount", ascending=False
        ).reset_index(drop=True)
