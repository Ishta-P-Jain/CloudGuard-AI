from rules.ec2.weak_security_group import WeakSecurityGroupRule


def test_broad_security_group_creates_finding():
    rule = WeakSecurityGroupRule()

    resource = {
        "group_id": "sg-wide-open",
        "group_name": "wide-open-security-group",
        "ingress_rules": [
            {
                "FromPort": 0,
                "ToPort": 65535,
                "IpProtocol": "-1",
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
    assert finding["rule_id"] == "EC2_WEAK_SECURITY_GROUP"
    assert finding["service"] == "EC2"
    assert finding["resource_id"] == "sg-wide-open"
    assert finding["severity"] == "CRITICAL"
    assert finding["title"] == "Security group allows broad network access"
    assert finding["description"] == "This security group allows broad network access from the internet."


def test_restricted_security_group_creates_no_finding():
    rule = WeakSecurityGroupRule()

    resource = {
        "group_id": "sg-restricted",
        "group_name": "restricted-security-group",
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