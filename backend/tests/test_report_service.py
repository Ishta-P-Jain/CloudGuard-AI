from app.services.report_service import build_fallback_remediation


def test_known_rule_returns_specific_steps():
    finding = {
        "rule_id": "EC2_OPEN_SSH",
        "service": "EC2",
        "title": "Security group allows SSH from the internet",
    }

    result = build_fallback_remediation(finding)

    assert "bastion host" in " ".join(result["remediation_steps"]).lower()
    assert result["estimated_effort"] == "Easy (5-15 minutes)"


def test_unknown_rule_returns_generic_steps():
    finding = {
        "rule_id": "UNKNOWN_RULE",
        "service": "CUSTOM",
        "title": "Some custom finding",
    }

    result = build_fallback_remediation(finding)

    assert len(result["remediation_steps"]) == 3
    assert "custom finding" in result["remediation_steps"][2].lower()