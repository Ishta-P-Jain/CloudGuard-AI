from rules.s3.public_write_access import PublicWriteAccessRule


def test_public_write_access_creates_finding():
    rule = PublicWriteAccessRule()

    resource = {
        "bucket_name": "demo-bucket",
        "public_write_access": True,
        "acl": "public-read-write",
    }

    findings = rule.evaluate(resource)

    assert len(findings) == 1
    finding = findings[0]
    assert finding["rule_id"] == "S3_PUBLIC_WRITE_ACCESS"
    assert finding["service"] == "S3"
    assert finding["resource_id"] == "demo-bucket"
    assert finding["severity"] == "CRITICAL"
    assert finding["title"] == "S3 bucket allows public write access"
    assert finding["description"] == "This S3 bucket allows public write access."


def test_private_bucket_creates_no_public_write_finding():
    rule = PublicWriteAccessRule()

    resource = {
        "bucket_name": "demo-bucket",
        "public_write_access": False,
        "acl": "private",
    }

    findings = rule.evaluate(resource)

    assert findings == []