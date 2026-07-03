from typing import Any, Dict, List

from rules.base_rule import BaseRule


class PublicWriteAccessRule(BaseRule):
    rule_id = "S3_PUBLIC_WRITE_ACCESS"
    service = "S3"
    title = "S3 bucket allows public write access"
    severity = "CRITICAL"

    def evaluate(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []

        bucket_name = resource.get("bucket_name", "unknown-bucket")
        public_write_access = _is_truthy(resource.get("public_write_access"))
        acl = str(resource.get("acl", "")).lower()

        if public_write_access or acl in {"public-read-write", "public-write"}:
            findings.append(
                self.build_finding(
                    resource_id=bucket_name,
                    description="This S3 bucket allows public write access.",
                    evidence={
                        "bucket_name": bucket_name,
                        "public_write_access": True,
                        "acl": acl or "unknown",
                    },
                )
            )

        return findings


def _is_truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y", "public"}
    if isinstance(value, (int, float)):
        return value != 0
    return bool(value)