from src.pipeline import run_pipeline
from src.validation import validate_processed_data


if __name__ == "__main__":
    result, output_path = run_pipeline()
    validate_processed_data(result)

    print("Validation: PASSED")
    print(f"Rows processed: {len(result)}")
    print(f"Output file: {output_path}")
