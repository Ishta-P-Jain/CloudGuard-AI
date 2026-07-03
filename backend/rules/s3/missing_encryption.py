from typing import Any, Dict, List

from rules.base_rule import BaseRule


class MissingEncryptionRule(BaseRule):
    rule_id = "S3_MISSING_ENCRYPTION"
    service = "S3"
    title = "S3 bucket does not use encryption"
    severity = "MEDIUM"

    def evaluate(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []

        bucket_name = resource.get("bucket_name", "unknown-bucket")
        encryption_enabled = _extract_bool(
            resource.get("encryption_enabled"),
            resource.get("encrypted"),
            resource.get("server_side_encryption"),
        )

        if not encryption_enabled:
            findings.append(
                self.build_finding(
                    resource_id=bucket_name,
                    description="This S3 bucket does not have encryption enabled.",
                    evidence={
                        "bucket_name": bucket_name,
                        "encryption_enabled": False,
                    },
                )
            )

        return findings


def _extract_bool(*values: Any) -> bool:
    for value in values:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"true", "1", "yes", "enabled"}:
                return True
            if normalized in {"false", "0", "no", "disabled"}:
                return False
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, dict):
            if value:
                return True
    return False