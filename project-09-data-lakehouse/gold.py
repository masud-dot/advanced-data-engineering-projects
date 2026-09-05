"""
Gold layer reference implementation for Apache Spark.

Production aggregation:
- Group sales by product.
- Calculate revenue.
- Calculate order count.
- Calculate average order value.
"""


def describe_gold_layer():
    return "Business-ready aggregated metrics stored in the Gold layer."


if __name__ == "__main__":
    print(describe_gold_layer())
