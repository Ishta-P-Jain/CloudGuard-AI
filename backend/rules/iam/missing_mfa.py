from typing import Any, Dict, List

from rules.base_rule import BaseRule


class MissingMfaRule(BaseRule):
    rule_id = "IAM_MISSING_MFA"
    service = "IAM"
    title = "IAM user does not use multi-factor authentication"
    severity = "HIGH"

    def evaluate(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []

        user_name = resource.get("user_name", "unknown-user")
        mfa_enabled = _extract_bool(
            resource.get("mfa_enabled"),
            resource.get("has_mfa"),
            resource.get("mfa_active"),
        )

        if not mfa_enabled:
            findings.append(
                self.build_finding(
                    resource_id=user_name,
                    description="This IAM user does not have MFA enabled.",
                    evidence={
                        "user_name": user_name,
                        "mfa_enabled": False,
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
    return False