from pathlib import Path

from pipelines.etl_pipeline import process_data


def run_pipeline(
    input_file="sample_data/sample_sales.csv",
    output_file="local_output/processed_sales.csv",
):
    """Execute the ETL pipeline and write the processed dataset."""
    result = process_data(input_file)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    return result, output_path


if __name__ == "__main__":
    result, output_path = run_pipeline()
    print(f"Pipeline completed successfully.")
    print(f"Rows processed: {len(result)}")
    print(f"Output: {output_path}")
