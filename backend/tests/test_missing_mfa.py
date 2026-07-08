from rules.iam.missing_mfa import MissingMfaRule


def test_user_without_mfa_creates_finding():
    rule = MissingMfaRule()

    resource = {
        "user_name": "demo-user",
        "mfa_enabled": False,
    }

    findings = rule.evaluate(resource)

    assert len(findings) == 1
    finding = findings[0]
    assert finding["rule_id"] == "IAM_MISSING_MFA"
    assert finding["service"] == "IAM"
    assert finding["resource_id"] == "demo-user"
    assert finding["severity"] == "HIGH"
    assert finding["title"] == "IAM user does not use multi-factor authentication"


def test_user_with_mfa_creates_no_finding():
    rule = MissingMfaRule()

    resource = {
        "user_name": "demo-user",
        "mfa_enabled": True,
    }

    findings = rule.evaluate(resource)

    assert findings == []