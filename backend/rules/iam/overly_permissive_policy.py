from typing import Any, Dict, Iterable, List

from rules.base_rule import BaseRule


class OverlyPermissivePolicyRule(BaseRule):
    rule_id = "IAM_OVERLY_PERMISSIVE_POLICY"
    service = "IAM"
    title = "IAM policy grants overly broad permissions"
    severity = "HIGH"

    def evaluate(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        policy_name = resource.get("policy_name", "unknown-policy")

        for index, statement in enumerate(_extract_statements(resource)):
            effect = str(statement.get("Effect", statement.get("effect", ""))).lower()
            actions = _to_list(statement.get("Action", statement.get("action")))
            resources = _to_list(statement.get("Resource", statement.get("resource")))

            if effect != "allow":
                continue

            if _is_overly_permissive(actions, resources):
                findings.append(
                    self.build_finding(
                        resource_id=policy_name,
                        description="This IAM policy grants broader access than necessary.",
                        evidence={
                            "policy_name": policy_name,
                            "statement_index": index,
                            "effect": statement.get("Effect", statement.get("effect", "Allow")),
                            "action": actions,
                            "resource": resources,
                        },
                    )
                )

        return findings


def _extract_statements(resource: Dict[str, Any]) -> List[Dict[str, Any]]:
    policy = resource.get("policy_document") or resource.get("policy") or {}
    if not isinstance(policy, dict):
        return []

    statements = policy.get("Statement", policy.get("statements", []))
    if isinstance(statements, dict):
        return [statements]
    if isinstance(statements, list):
        return [statement for statement in statements if isinstance(statement, dict)]
    return []


def _to_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _is_overly_permissive(actions: Iterable[Any], resources: Iterable[Any]) -> bool:
    normalized_actions = [str(action).lower() for action in actions]
    normalized_resources = [str(resource).lower() for resource in resources]

    if "*" in normalized_actions or "*" in normalized_resources:
        return True

    if any(action.endswith(":*") for action in normalized_actions):
        return True

    if any(resource == "*" for resource in normalized_resources):
        return True

    return False