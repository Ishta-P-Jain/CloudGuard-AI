from typing import Any, Dict, List

from rules.base_rule import BaseRule


class WeakSecurityGroupRule(BaseRule):
    rule_id = "EC2_WEAK_SECURITY_GROUP"
    service = "EC2"
    title = "Security group allows broad network access"
    severity = "CRITICAL"

    def evaluate(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []

        group_id = resource.get("group_id", "unknown-group")
        group_name = resource.get("group_name", group_id)

        for index, rule in enumerate(_extract_ingress_rules(resource)):
            from_port = _safe_int(rule.get("FromPort", rule.get("from_port")))
            to_port = _safe_int(rule.get("ToPort", rule.get("to_port")))
            protocol = str(rule.get("IpProtocol", rule.get("protocol", ""))).lower()
            cidrs = _extract_cidrs(rule)

            if _is_broad_rule(from_port, to_port, protocol) and _has_public_cidr(cidrs):
                findings.append(
                    self.build_finding(
                        resource_id=group_id,
                        description="This security group allows broad network access from the internet.",
                        evidence={
                            "group_id": group_id,
                            "group_name": group_name,
                            "rule_index": index,
                            "from_port": from_port,
                            "to_port": to_port,
                            "protocol": protocol,
                            "cidrs": cidrs,
                        },
                    )
                )

        return findings


def _extract_ingress_rules(resource: Dict[str, Any]) -> List[Dict[str, Any]]:
    rules = resource.get("ingress_rules") or resource.get("IpPermissions") or []
    if isinstance(rules, list):
        return [rule for rule in rules if isinstance(rule, dict)]
    return []


def _extract_cidrs(rule: Dict[str, Any]) -> List[str]:
    cidrs: List[str] = []
    for item in rule.get("IpRanges", rule.get("ip_ranges", [])) or []:
        if isinstance(item, dict) and item.get("CidrIp"):
            cidrs.append(str(item["CidrIp"]))
        elif isinstance(item, str):
            cidrs.append(item)
    return cidrs


def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return -1


def _is_broad_rule(from_port: int, to_port: int, protocol: str) -> bool:
    if protocol in {"-1", "all"}:
        return True
    return from_port == 0 and to_port == 65535


def _has_public_cidr(cidrs: List[str]) -> bool:
    public_values = {"0.0.0.0/0", "::/0"}
    return any(str(cidr).strip() in public_values for cidr in cidrs)