from rules.s3.missing_encryption import MissingEncryptionRule


def test_bucket_without_encryption_creates_finding():
    rule = MissingEncryptionRule()

    resource = {
        "bucket_name": "demo-bucket",
        "encryption_enabled": False,
    }

    findings = rule.evaluate(resource)

    assert len(findings) == 1
    finding = findings[0]
    assert finding["rule_id"] == "S3_MISSING_ENCRYPTION"
    assert finding["service"] == "S3"
    assert finding["resource_id"] == "demo-bucket"
    assert finding["severity"] == "MEDIUM"
    assert finding["title"] == "S3 bucket does not use encryption"
    assert finding["description"] == "This S3 bucket does not have encryption enabled."


def test_bucket_with_encryption_creates_no_finding():
    rule = MissingEncryptionRule()

    resource = {
        "bucket_name": "demo-bucket",
        "encryption_enabled": True,
    }

    findings = rule.evaluate(resource)

    assert findings == []