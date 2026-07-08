from rules.ec2.public_instance import PublicInstanceRule


def test_public_instance_creates_finding():
    rule = PublicInstanceRule()

    resource = {
        "instance_id": "i-1234567890",
        "public_ip_address": "18.12.34.56",
    }

    findings = rule.evaluate(resource)

    assert len(findings) == 1
    finding = findings[0]
    assert finding["rule_id"] == "EC2_PUBLIC_INSTANCE"
    assert finding["service"] == "EC2"
    assert finding["resource_id"] == "i-1234567890"
    assert finding["severity"] == "MEDIUM"
    assert finding["title"] == "EC2 instance has a public IP address"
    assert finding["description"] == "This EC2 instance is reachable from the internet."


def test_private_instance_creates_no_finding():
    rule = PublicInstanceRule()

    resource = {
        "instance_id": "i-1234567890",
        "public_ip_address": None,
        "publicly_accessible": False,
    }

    findings = rule.evaluate(resource)

    assert findings == []