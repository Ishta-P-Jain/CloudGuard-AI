from app.schemas.scan_schema import ScanSummary
from app.services.risk_service import calculate_score


def test_scan_summary_matches_schema_shape():
    result = calculate_score(
        [
            {"severity": "CRITICAL"},
            {"severity": "HIGH"},
            {"severity": "MEDIUM"},
        ]
    )

    summary = ScanSummary(**result["summary"])

    assert summary.total == 3
    assert summary.critical == 1
    assert summary.high == 1
    assert summary.medium == 1
    assert summary.low == 0


def test_empty_scan_summary_is_valid():
    result = calculate_score([])
    summary = ScanSummary(**result["summary"])

    assert summary.total == 0
    assert summary.critical == 0
    assert summary.high == 0
    assert summary.medium == 0
    assert summary.low == 0