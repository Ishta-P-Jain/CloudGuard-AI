from rules.rule_engine import run_scan


def test_rule_engine_combines_multiple_findings():
    resources = {
        "s3_buckets": [
            {
                "bucket_name": "public-bucket",
                "public_access": True,
                "public_write_access": True,
                "encryption_enabled": False,
            }
        ],
        "iam_users": [
            {
                "user_name": "demo-user",
                "mfa_enabled": False,
            }
        ],
        "iam_policies": [
            {
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
        ],
        "ec2_security_groups": [
            {
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
        ],
        "ec2_instances": [
            {
                "instance_id": "i-1234567890",
                "public_ip_address": "18.12.34.56",
            }
        ],
    }

    findings = run_scan(resources)
    rule_ids = {finding["rule_id"] for finding in findings}

    assert "S3_PUBLIC_BUCKET_ACCESS" in rule_ids
    assert "S3_PUBLIC_WRITE_ACCESS" in rule_ids
    assert "S3_MISSING_ENCRYPTION" in rule_ids
    assert "IAM_MISSING_MFA" in rule_ids
    assert "IAM_ADMIN_ACCESS_DETECTION" in rule_ids
    assert "EC2_OPEN_SSH" in rule_ids
    assert "EC2_PUBLIC_INSTANCE" in rule_ids