from rules.iam.admin_access_detection import AdminAccessDetectionRule


def test_admin_policy_creates_finding():
    rule = AdminAccessDetectionRule()

    resource = {
        "policy_name": "admin-policy",
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
    assert finding["rule_id"] == "IAM_ADMIN_ACCESS_DETECTION"
    assert finding["service"] == "IAM"
    assert finding["resource_id"] == "admin-policy"
    assert finding["severity"] == "CRITICAL"
    assert finding["title"] == "IAM policy grants administrator access"


def test_non_admin_policy_creates_no_finding():
    rule = AdminAccessDetectionRule()

    resource = {
        "policy_name": "limited-policy",
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