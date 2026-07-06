from typing import Any, Dict, List

from rules.base_rule import BaseRule


class PublicInstanceRule(BaseRule):
    rule_id = "EC2_PUBLIC_INSTANCE"
    service = "EC2"
    title = "EC2 instance has a public IP address"
    severity = "MEDIUM"

    def evaluate(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []

        instance_id = resource.get("instance_id", "unknown-instance")
        public_ip = resource.get("public_ip_address") or resource.get("public_ip")
        publicly_accessible = _is_truthy(resource.get("publicly_accessible")) or _is_truthy(
            resource.get("associate_public_ip_address")
        )

        if public_ip or publicly_accessible:
            findings.append(
                self.build_finding(
                    resource_id=instance_id,
                    description="This EC2 instance is reachable from the internet.",
                    evidence={
                        "instance_id": instance_id,
                        "public_ip_address": public_ip,
                        "publicly_accessible": publicly_accessible,
                    },
                )
            )

        return findings


def _is_truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    if isinstance(value, (int, float)):
        return value != 0
    return bool(value)