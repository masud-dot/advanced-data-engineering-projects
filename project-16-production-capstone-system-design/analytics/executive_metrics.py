import pandas as pd


class ExecutiveMetrics:
    def calculate(self, transactions: pd.DataFrame) -> dict:
        total = float(transactions["amount_usd"].sum())
        count = int(len(transactions))

        return {
            "transaction_count": count,
            "total_transaction_value": round(total, 2),
            "average_transaction_value": round(total / count, 2)
            if count
            else 0.0,
            "fraud_transactions": int(
                transactions.get("fraud_flag", pd.Series(dtype=bool)).sum()
            ),
        }
