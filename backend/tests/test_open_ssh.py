from rules.ec2.open_ssh import OpenSshRule


def test_open_ssh_creates_finding():
    rule = OpenSshRule()

    resource = {
        "group_id": "sg-12345",
        "group_name": "demo-security-group",
        "ingress_rules": [
            {
                "FromPort": 22,
                "ToPort": 22,
                "IpProtocol": "tcp",
                "IpRanges": [
                    {
                        "CidrIp": "0.0.0.0/0",
                    }
                ],
            }
        ],
    }

    findings = rule.evaluate(resource)

    assert len(findings) == 1
    finding = findings[0]
    assert finding["rule_id"] == "EC2_OPEN_SSH"
    assert finding["service"] == "EC2"
    assert finding["resource_id"] == "sg-12345"
    assert finding["severity"] == "HIGH"
    assert finding["title"] == "Security group allows SSH from the internet"
    assert finding["description"] == "This security group allows SSH from the internet."


def test_private_ssh_rule_creates_no_finding():
    rule = OpenSshRule()

    resource = {
        "group_id": "sg-12345",
        "group_name": "demo-security-group",
        "ingress_rules": [
            {
                "FromPort": 22,
                "ToPort": 22,
                "IpProtocol": "tcp",
                "IpRanges": [
                    {
                        "CidrIp": "10.0.0.0/24",
                    }
                ],
            }
        ],
    }

    findings = rule.evaluate(resource)

    assert findings == []