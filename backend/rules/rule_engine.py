from typing import Any, Dict, List

from rules.ec2.open_rdp import OpenRdpRule
from rules.ec2.open_ssh import OpenSshRule
from rules.ec2.public_instance import PublicInstanceRule
from rules.ec2.weak_security_group import WeakSecurityGroupRule
from rules.iam.admin_access_detection import AdminAccessDetectionRule
from rules.iam.missing_mfa import MissingMfaRule
from rules.iam.overly_permissive_policy import OverlyPermissivePolicyRule
from rules.s3.missing_encryption import MissingEncryptionRule
from rules.s3.public_bucket_access import PublicBucketAccessRule
from rules.s3.public_write_access import PublicWriteAccessRule


def run_scan(resources: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    s3_buckets = _ensure_list(resources.get("s3_buckets"))
    iam_users = _ensure_list(resources.get("iam_users"))
    iam_policies = _ensure_list(resources.get("iam_policies"))
    ec2_security_groups = _ensure_list(resources.get("ec2_security_groups"))
    ec2_instances = _ensure_list(resources.get("ec2_instances"))

    s3_rules = [
        PublicBucketAccessRule(),
        PublicWriteAccessRule(),
        MissingEncryptionRule(),
    ]

    iam_user_rules = [MissingMfaRule()]
    iam_policy_rules = [
        OverlyPermissivePolicyRule(),
        AdminAccessDetectionRule(),
    ]

    ec2_security_group_rules = [
        OpenSshRule(),
        OpenRdpRule(),
        WeakSecurityGroupRule(),
    ]

    ec2_instance_rules = [PublicInstanceRule()]

    for bucket in s3_buckets:
        for rule in s3_rules:
            findings.extend(rule.evaluate(bucket))

    for user in iam_users:
        for rule in iam_user_rules:
            findings.extend(rule.evaluate(user))

    for policy in iam_policies:
        for rule in iam_policy_rules:
            findings.extend(rule.evaluate(policy))

    for security_group in ec2_security_groups:
        for rule in ec2_security_group_rules:
            findings.extend(rule.evaluate(security_group))

    for instance in ec2_instances:
        for rule in ec2_instance_rules:
            findings.extend(rule.evaluate(instance))

    return findings


def _ensure_list(value: Any) -> List[Dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []