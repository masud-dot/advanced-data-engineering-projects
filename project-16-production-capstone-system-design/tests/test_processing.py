import pandas as pd

from processing.stream_processor import SimulatedSparkProcessor


def test_processing_removes_invalid_and_duplicates():
    df = pd.DataFrame(
        [
            {
                "transaction_id": "1",
                "customer_id": 1001,
                "transaction_timestamp": "2026-01-01T10:00:00",
                "merchant_category": "Grocery",
                "amount": 100,
                "currency": "USD",
                "status": "COMPLETED",
            },
            {
                "transaction_id": "1",
                "customer_id": 1001,
                "transaction_timestamp": "2026-01-01T10:00:00",
                "merchant_category": "Grocery",
                "amount": 100,
                "currency": "USD",
                "status": "COMPLETED",
            },
            {
                "transaction_id": "2",
                "customer_id": 1002,
                "transaction_timestamp": "2026-01-01T10:00:00",
                "merchant_category": "Grocery",
                "amount": -10,
                "currency": "USD",
                "status": "COMPLETED",
            },
        ]
    )

    result = SimulatedSparkProcessor().transform(df)

    assert len(result) == 1
    assert result.iloc[0]["transaction_id"] == "1"
