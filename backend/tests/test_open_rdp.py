from rules.ec2.open_rdp import OpenRdpRule


def test_open_rdp_creates_finding():
    rule = OpenRdpRule()

    resource = {
        "group_id": "sg-67890",
        "group_name": "windows-security-group",
        "ingress_rules": [
            {
                "FromPort": 3389,
                "ToPort": 3389,
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
    assert finding["rule_id"] == "EC2_OPEN_RDP"
    assert finding["service"] == "EC2"
    assert finding["resource_id"] == "sg-67890"
    assert finding["severity"] == "HIGH"
    assert finding["title"] == "Security group allows RDP from the internet"
    assert finding["description"] == "This security group allows RDP from the internet."


def test_private_rdp_rule_creates_no_finding():
    rule = OpenRdpRule()

    resource = {
        "group_id": "sg-67890",
        "group_name": "windows-security-group",
        "ingress_rules": [
            {
                "FromPort": 3389,
                "ToPort": 3389,
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