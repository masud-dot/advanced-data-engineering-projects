import json

from pipelines.customer360_pipeline import Customer360Pipeline


def main():
    print("=" * 70)
    print("CUSTOMER 360 UNIFIED ANALYTICS PLATFORM")
    print("=" * 70)

    pipeline = Customer360Pipeline()
    result = pipeline.run()

    summary = result["summary"]
    quality = result["quality"]["profile_quality"]
    monitoring = result["monitoring"]

    print("\nCUSTOMER 360 SUMMARY")
    print("-" * 70)
    print(f"Customers:              {summary['total_customers']}")
    print(f"Orders:                 {summary['total_orders']}")
    print(f"Units:                  {summary['total_units']}")
    print(f"Total Revenue:          ${summary['total_revenue']:,.2f}")
    print(
        f"Average Customer Value: "
        f"${summary['average_customer_lifetime_value']:,.2f}"
    )
    print(
        f"Average Order Value:    "
        f"${summary['average_order_value']:,.2f}"
    )
    print(
        f"Average Engagement:     "
        f"{summary['average_engagement_score']:.2f}"
    )
    print(f"VIP Customers:          {summary['vip_customers']}")
    print(f"At-Risk Customers:      {summary['at_risk_customers']}")

    print("\nQUALITY")
    print("-" * 70)
    print(f"Quality Score:           {quality['score']:.2f}%")
    print(f"Quality Status:          {quality['status']}")

    print("\nMONITORING")
    print("-" * 70)
    print(
        f"Input Records:           "
        f"{monitoring['input_records']}"
    )
    print(
        f"Output Profiles:         "
        f"{monitoring['output_records']}"
    )
    print(
        f"Runtime:                 "
        f"{monitoring['runtime_seconds']:.4f}s"
    )
    print(f"Pipeline Status:         {monitoring['status']}")

    if monitoring["alerts"]:
        print("\nALERTS")
        for alert in monitoring["alerts"]:
            print(f"- {alert}")

    print("\nTOP CUSTOMERS")
    print("-" * 70)
    print(
        result["top_customers"][
            [
                "customer_id",
                "customer_name",
                "customer_segment",
                "lifetime_value",
            ]
        ].to_string(index=False)
    )

    print("\nSEGMENT SUMMARY")
    print("-" * 70)
    print(
        result["segment_summary"].to_string(index=False)
    )

    print("\nPIPELINE RESULT")
    print("-" * 70)
    print(json.dumps({
        "status": monitoring["status"],
        "quality_score": quality["score"],
        "customers": summary["total_customers"],
        "orders": summary["total_orders"],
        "revenue": summary["total_revenue"],
    }, indent=2))

    print("\n" + "=" * 70)
    print("CUSTOMER 360 PIPELINE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
