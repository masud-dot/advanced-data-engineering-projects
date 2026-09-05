import pandas as pd

from storage.iceberg_table import LocalIcebergTable


def test_local_iceberg_table(tmp_path):
    table = LocalIcebergTable(str(tmp_path))

    df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": ["A", "B"],
        }
    )

    table.write("silver", "test_table", df)
    result = table.snapshot("silver", "test_table")

    assert len(result) == 2
    assert list(result["value"]) == ["A", "B"]
