from rules.s3.public_bucket_access import PublicBucketAccessRule


def test_public_bucket_creates_finding():
    rule = PublicBucketAccessRule()

    resource = {
        "bucket_name": "demo-bucket",
        "public_access": True,
    }

    findings = rule.evaluate(resource)

    assert len(findings) == 1
    finding = findings[0]
    assert finding["rule_id"] == "S3_PUBLIC_BUCKET_ACCESS"
    assert finding["service"] == "S3"
    assert finding["resource_id"] == "demo-bucket"
    assert finding["severity"] == "HIGH"
    assert finding["title"] == "S3 bucket allows public read access"
    assert finding["description"] == "This S3 bucket can be read by anyone on the internet."


def test_private_bucket_creates_no_finding():
    rule = PublicBucketAccessRule()

    resource = {
        "bucket_name": "demo-bucket",
        "public_access": False,
    }

    findings = rule.evaluate(resource)

    assert findings == [] 