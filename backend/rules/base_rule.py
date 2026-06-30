from typing import Any, Dict, List


class BaseRule:
    rule_id = ""
    service = ""
    title = ""
    severity = "LOW"

    def evaluate(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError("Each security rule must implement evaluate().")

    def build_finding(
        self,
        resource_id: str,
        description: str,
        evidence: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "service": self.service,
            "resource_id": resource_id,
            "title": self.title,
            "severity": self.severity,
            "description": description,
            "evidence": evidence,
        }