from rules.iam.overly_permissive_policy import OverlyPermissivePolicyRule


def test_wildcard_policy_creates_finding():
    rule = OverlyPermissivePolicyRule()

    resource = {
        "policy_name": "demo-policy",
        "policy_document": {
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "*",
                    "Resource": "*",
                }
            ]
        },
    }

    findings = rule.evaluate(resource)

    assert len(findings) == 1
    finding = findings[0]
    assert finding["rule_id"] == "IAM_OVERLY_PERMISSIVE_POLICY"
    assert finding["service"] == "IAM"
    assert finding["resource_id"] == "demo-policy"
    assert finding["severity"] == "HIGH"
    assert finding["title"] == "IAM policy grants overly broad permissions"


def test_limited_policy_creates_no_finding():
    rule = OverlyPermissivePolicyRule()

    resource = {
        "policy_name": "demo-policy",
        "policy_document": {
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["s3:GetObject"],
                    "Resource": ["arn:aws:s3:::demo-bucket/*"],
                }
            ]
        },
    }

    findings = rule.evaluate(resource)

    assert findings == []