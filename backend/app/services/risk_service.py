from typing import Any, Dict, List


SEVERITY_POINTS = {
    "CRITICAL": 25,
    "HIGH": 15,
    "MEDIUM": 8,
    "LOW": 3,
}


def calculate_score(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_risk_points = 0
    summary = {
        "total": len(findings),
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for finding in findings:
        severity = str(finding.get("severity", "LOW")).upper()
        severity_key = severity.lower()

        if severity_key in summary:
            summary[severity_key] += 1

        total_risk_points += SEVERITY_POINTS.get(severity, 0)

    score = max(0, 100 - total_risk_points)

    return {
        "score": score,
        "summary": summary,
    }