from customer360.profile_builder import Customer360ProfileBuilder
from customer360.segmentation import CustomerSegmentation


def test_profile_builder():
    import pandas as pd

    profile = pd.DataFrame(
        {
            "customer_id": [101],
            "customer_name": ["Alice"],
            "email": ["alice@example.com"],
            "region": ["North"],
            "signup_date": [pd.Timestamp("2024-01-15")],
            "order_count": [3],
            "total_revenue": [1860],
            "total_units": [5],
            "average_order_value": [620],
            "first_order_date": [pd.Timestamp("2026-01-02")],
            "last_order_date": [pd.Timestamp("2026-01-23")],
            "activity_count": [3],
            "login_count": [1],
            "product_view_count": [0],
            "support_ticket_count": [1],
            "email_open_count": [0],
            "activity_purchase_count": [1],
            "preferred_category": ["Electronics"],
        }
    )

    result = Customer360ProfileBuilder().build(profile)

    assert len(result) == 1
    assert result.iloc[0]["lifetime_value"] == 1860
    assert result.iloc[0]["customer_status"] == "ACTIVE"
    assert result.iloc[0]["profile_completeness"] == 100


def test_segmentation():
    import pandas as pd

    profile = pd.DataFrame(
        {
            "customer_id": [101, 102],
            "lifetime_value": [2500, 500],
            "order_count": [4, 1],
            "engagement_score": [10, 2],
            "recency_days": [5, 5],
            "customer_age_days": [700, 700],
        }
    )

    result = CustomerSegmentation().segment(profile)

    assert result.loc[0, "customer_segment"] == "VIP"
    assert result.loc[1, "customer_segment"] == "ACTIVE"
