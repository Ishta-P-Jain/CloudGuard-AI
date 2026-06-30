from typing import Any, Dict, List

from rules.base_rule import BaseRule


class PublicBucketAccessRule(BaseRule):
    rule_id = "S3_PUBLIC_BUCKET_ACCESS"
    service = "S3"
    title = "S3 bucket allows public read access"
    severity = "HIGH"

    def evaluate(self, resource: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []

        bucket_name = resource.get("bucket_name", "unknown-bucket")
        public_access = resource.get("public_access", False)

        if public_access:
            findings.append(
                self.build_finding(
                    resource_id=bucket_name,
                    description="This S3 bucket can be read by anyone on the internet.",
                    evidence={
                        "bucket_name": bucket_name,
                        "public_access": True,
                    },
                )
            )

        return findings