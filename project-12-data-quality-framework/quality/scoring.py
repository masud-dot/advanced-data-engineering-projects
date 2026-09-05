from dataclasses import dataclass
from typing import Dict


@dataclass
class QualityScore:
    score: float
    passed: bool
    component_scores: Dict[str, float]


def calculate_quality_score(
    component_scores: Dict[str, float],
    weights: Dict[str, float],
    minimum_score: float = 0.95,
) -> QualityScore:
    if not component_scores:
        return QualityScore(
            score=0.0,
            passed=False,
            component_scores={},
        )

    weighted_score = sum(
        component_scores.get(name, 0.0) * weight
        for name, weight in weights.items()
    )

    total_weight = sum(weights.values())

    score = (
        weighted_score / total_weight
        if total_weight
        else 0.0
    )

    score = round(score, 4)

    return QualityScore(
        score=score,
        passed=score >= minimum_score,
        component_scores=component_scores,
    )
