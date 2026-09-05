from pathlib import Path
from typing import Any, Dict

import pandas as pd
import yaml

from quality.business_rules import validate_business_rules
from quality.completeness import validate_completeness
from quality.duplicates import validate_duplicates
from quality.freshness import validate_freshness
from quality.referential_integrity import validate_referential_integrity
from quality.schema import validate_schema
from quality.scoring import QualityScore, calculate_quality_score


class DataQualityEngine:
    def __init__(self, config_file: str):
        with open(config_file, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    def validate(
        self,
        df: pd.DataFrame,
        reference_data: Dict[str, pd.DataFrame] | None = None,
    ) -> Dict[str, Any]:
        reference_data = reference_data or {}

        schema_config = self.config["schema"]
        completeness_config = self.config["completeness"]
        duplicate_config = self.config["duplicates"]
        business_config = self.config["business_rules"]
        freshness_config = self.config["freshness"]
        reference_config = self.config["referential_integrity"]
        scoring_config = self.config["scoring"]

        schema_result = validate_schema(
            df,
            schema_config["required_columns"],
        )

        completeness_result = validate_completeness(
            df,
            completeness_config["required_columns"],
            completeness_config["minimum_completeness_score"],
        )

        duplicate_result = validate_duplicates(
            df,
            duplicate_config["key_columns"],
        )

        business_result = validate_business_rules(
            df,
            amount_min=business_config["amount"]["min"],
            allowed_statuses=business_config["status"]["allowed_values"],
        )

        freshness_result = validate_freshness(
            df,
            freshness_config["timestamp_column"],
            freshness_config["max_age_days"],
        )

        customer_reference = reference_data.get("customer_id")

        if customer_reference is not None:
            reference_result = validate_referential_integrity(
                df,
                "customer_id",
                customer_reference,
                reference_config["customer_id"]["reference_column"],
            )
        else:
            reference_result = None

        component_scores = {
            "schema": 1.0 if schema_result.passed else 0.0,
            "completeness": completeness_result.score,
            "duplicate": 1.0 if duplicate_result.passed else 0.0,
            "business_rule": 1.0 if business_result.passed else 0.0,
            "freshness": 1.0 if freshness_result.passed else 0.0,
            "referential_integrity": (
                1.0
                if reference_result is not None and reference_result.passed
                else 0.0
            ),
        }

        weights = {
            "schema": scoring_config["schema_weight"],
            "completeness": scoring_config["completeness_weight"],
            "duplicate": scoring_config["duplicate_weight"],
            "business_rule": scoring_config["business_rule_weight"],
            "freshness": scoring_config["freshness_weight"],
            "referential_integrity": (
                scoring_config["referential_integrity_weight"]
            ),
        }

        quality_score: QualityScore = calculate_quality_score(
            component_scores,
            weights,
            scoring_config["minimum_quality_score"],
        )

        checks = {
            "schema": schema_result,
            "completeness": completeness_result,
            "duplicates": duplicate_result,
            "business_rules": business_result,
            "freshness": freshness_result,
            "referential_integrity": reference_result,
        }

        return {
            "dataset": self.config["dataset"]["name"],
            "row_count": len(df),
            "checks": checks,
            "quality_score": quality_score,
            "passed": quality_score.passed,
        }
