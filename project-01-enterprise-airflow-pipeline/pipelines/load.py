import os

from sqlalchemy import create_engine, text


def load_data(df) -> None:
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Configure it before running the load step."
        )

    if "order_id" not in df.columns:
        raise ValueError("order_id is required for idempotent loading.")

    engine = create_engine(database_url)

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS sales_data (
                    order_id BIGINT PRIMARY KEY,
                    customer_name TEXT,
                    product_name TEXT,
                    quantity BIGINT,
                    price BIGINT,
                    order_date DATE,
                    region TEXT,
                    total_amount BIGINT
                )
                """
            )
        )

        for record in df.to_dict(orient="records"):
            connection.execute(
                text(
                    """
                    INSERT INTO sales_data (
                        order_id,
                        customer_name,
                        product_name,
                        quantity,
                        price,
                        order_date,
                        region,
                        total_amount
                    )
                    VALUES (
                        :order_id,
                        :customer_name,
                        :product_name,
                        :quantity,
                        :price,
                        :order_date,
                        :region,
                        :total_amount
                    )
                    ON CONFLICT (order_id)
                    DO UPDATE SET
                        customer_name = EXCLUDED.customer_name,
                        product_name = EXCLUDED.product_name,
                        quantity = EXCLUDED.quantity,
                        price = EXCLUDED.price,
                        order_date = EXCLUDED.order_date,
                        region = EXCLUDED.region,
                        total_amount = EXCLUDED.total_amount
                    """
                ),
                record,
            )
