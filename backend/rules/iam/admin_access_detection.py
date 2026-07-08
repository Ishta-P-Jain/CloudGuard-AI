from typing import Any, Dict, List

from rules.base_rule import BaseRule


class AdminAccessDetectionRule(BaseRule):
    rule_id = "IAM_ADMIN_ACCESS_DETECTION"
    service = "IAM"
    title = "IAM policy grants administrator access"
    severity = "CRITICAL"

    def evaluate(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        policy_name = resource.get("policy_name", "unknown-policy")

        for index, statement in enumerate(_extract_statements(resource)):
            effect = str(statement.get("Effect", statement.get("effect", ""))).lower()
            actions = _to_list(statement.get("Action", statement.get("action")))
            resources = _to_list(statement.get("Resource", statement.get("resource")))

            if effect != "allow":
                continue

            if _looks_like_admin_access(actions, resources):
                findings.append(
                    self.build_finding(
                        resource_id=policy_name,
                        description="This IAM policy gives administrator-level access.",
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


def _looks_like_admin_access(actions: List[Any], resources: List[Any]) -> bool:
    normalized_actions = [str(action).lower() for action in actions]
    normalized_resources = [str(resource).lower() for resource in resources]

    if "*" in normalized_actions and "*" in normalized_resources:
        return True

    if any(action == "*" for action in normalized_actions) and any(
        resource == "*" for resource in normalized_resources
    ):
        return True

    admin_action_patterns = {
        "iam:*",
        "ec2:*",
        "s3:*",
        "lambda:*",
        "ecs:*",
        "rds:*",
        "cloudformation:*",
    }

    if any(action in admin_action_patterns for action in normalized_actions) and "*" in normalized_resources:
        return True

    if "administratoraccess" in " ".join(normalized_actions + normalized_resources):
        return True

    return False