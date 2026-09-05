from quality.scoring import calculate_quality_score


def test_quality_score_passes_for_perfect_data():
    components = {
        "schema": 1.0,
        "completeness": 1.0,
        "duplicate": 1.0,
        "business_rule": 1.0,
        "freshness": 1.0,
        "referential_integrity": 1.0,
    }

    weights = {
        "schema": 0.20,
        "completeness": 0.20,
        "duplicate": 0.15,
        "business_rule": 0.20,
        "freshness": 0.10,
        "referential_integrity": 0.15,
    }

    result = calculate_quality_score(
        components,
        weights,
        minimum_score=0.95,
    )

    assert result.score == 1.0
    assert result.passed is True


def test_quality_score_fails_for_poor_data():
    components = {
        "schema": 1.0,
        "completeness": 0.5,
        "duplicate": 0.0,
        "business_rule": 0.0,
        "freshness": 1.0,
        "referential_integrity": 0.0,
    }

    weights = {
        "schema": 0.20,
        "completeness": 0.20,
        "duplicate": 0.15,
        "business_rule": 0.20,
        "freshness": 0.10,
        "referential_integrity": 0.15,
    }

    result = calculate_quality_score(
        components,
        weights,
        minimum_score=0.95,
    )

    assert result.score < 0.95
    assert result.passed is False
