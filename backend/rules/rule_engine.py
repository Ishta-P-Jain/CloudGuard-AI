from typing import Any, Dict, List

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

    for bucket in s3_buckets:
        for rule in s3_rules:
            findings.extend(rule.evaluate(bucket))

    for user in iam_users:
        for rule in iam_user_rules:
            findings.extend(rule.evaluate(user))

    for policy in iam_policies:
        for rule in iam_policy_rules:
            findings.extend(rule.evaluate(policy))

    return findings


def _ensure_list(value: Any) -> List[Dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []