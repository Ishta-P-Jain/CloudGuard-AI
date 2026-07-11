from app.services.risk_service import calculate_score


def test_calculate_score_counts_severities_correctly():
    findings = [
        {"severity": "CRITICAL"},
        {"severity": "HIGH"},
        {"severity": "MEDIUM"},
        {"severity": "LOW"},
    ]

    result = calculate_score(findings)

    assert result["score"] == 49
    assert result["summary"] == {
        "total": 4,
        "critical": 1,
        "high": 1,
        "medium": 1,
        "low": 1,
    }


def test_unknown_severity_does_not_break_scoring():
    findings = [
        {"severity": "HIGH"},
        {"severity": "MYSTERY"},
    ]

    result = calculate_score(findings)

    assert result["score"] == 85
    assert result["summary"] == {
        "total": 2,
        "critical": 0,
        "high": 1,
        "medium": 0,
        "low": 0,
    }