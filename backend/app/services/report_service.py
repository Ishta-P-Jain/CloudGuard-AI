from typing import Any, Dict, List


FALLBACK_REMEDIATION_BY_RULE = {
    "S3_PUBLIC_BUCKET_ACCESS": [
        "Remove public read permissions from the bucket.",
        "Enable S3 Block Public Access.",
        "Allow access only to trusted IAM users or roles.",
    ],
    "S3_PUBLIC_WRITE_ACCESS": [
        "Remove public write permissions from the bucket.",
        "Restrict write access to approved IAM roles only.",
        "Review the bucket ACL and policy for public access.",
    ],
    "S3_MISSING_ENCRYPTION": [
        "Enable default encryption on the bucket.",
        "Use SSE-S3 or SSE-KMS for stored objects.",
        "Confirm new objects are encrypted automatically.",
    ],
    "IAM_MISSING_MFA": [
        "Enable MFA for the IAM user.",
        "Use MFA for all privileged accounts.",
        "Review account access regularly.",
    ],
    "IAM_OVERLY_PERMISSIVE_POLICY": [
        "Replace wildcard permissions with least-privilege actions.",
        "Limit resources to the exact bucket, role, or instance required.",
        "Review the policy with a security checklist.",
    ],
    "IAM_ADMIN_ACCESS_DETECTION": [
        "Reduce administrator access to only the people who truly need it.",
        "Split admin tasks into smaller IAM roles where possible.",
        "Audit who can create or attach admin policies.",
    ],
    "EC2_OPEN_SSH": [
        "Restrict SSH access to trusted IP addresses only.",
        "Use a bastion host or VPN instead of open internet access.",
        "Close port 22 if it is not required.",
    ],
    "EC2_OPEN_RDP": [
        "Restrict RDP access to trusted IP addresses only.",
        "Use VPN access instead of public RDP exposure.",
        "Close port 3389 if it is not needed.",
    ],
    "EC2_PUBLIC_INSTANCE": [
        "Remove the public IP if internet access is not required.",
        "Place the instance in a private subnet when possible.",
        "Use a load balancer or bastion host for controlled access.",
    ],
    "EC2_WEAK_SECURITY_GROUP": [
        "Remove 0.0.0.0/0 from the security group.",
        "Open only the ports the application actually needs.",
        "Review inbound rules regularly.",
    ],
}


FALLBACK_EXPLANATIONS_FRIENDLY = {
    "S3_PUBLIC_BUCKET_ACCESS": "This S3 bucket allows public read access. Anyone on the internet can list and read the files stored inside.",
    "S3_PUBLIC_WRITE_ACCESS": "This S3 bucket allows public write access. Anyone can modify, upload, or delete files in the bucket.",
    "S3_MISSING_ENCRYPTION": "This S3 bucket does not enforce server-side encryption. Stored files are written in plaintext.",
    "IAM_MISSING_MFA": "This IAM user is missing Multi-Factor Authentication (MFA), making the account vulnerable to password theft.",
    "IAM_OVERLY_PERMISSIVE_POLICY": "This IAM policy grants overly broad permissions (using wildcards like '*'), violating least privilege.",
    "IAM_ADMIN_ACCESS_DETECTION": "This policy grants full administrative access. It should only be attached to verified administrators.",
    "EC2_OPEN_SSH": "The security group allows public inbound SSH traffic (port 22) from any IP, exposing the server to brute-force attacks.",
    "EC2_OPEN_RDP": "The security group allows public RDP traffic (port 3389) from any IP, exposing Remote Desktop to brute-force attacks.",
    "EC2_PUBLIC_INSTANCE": "This EC2 instance has a public IP address and is exposed directly to the internet.",
    "EC2_WEAK_SECURITY_GROUP": "This security group allows wide open ingress access on sensitive ports."
}


def build_fallback_remediation(finding: Dict[str, Any]) -> Dict[str, Any]:
    rule_id = str(finding.get("rule_id", "")).upper()
    service = str(finding.get("service", "")).upper()
    title = str(finding.get("title", "")).strip()

    steps = FALLBACK_REMEDIATION_BY_RULE.get(rule_id)
    if steps is None:
        steps = _generic_steps(service, title)

    explanation = FALLBACK_EXPLANATIONS_FRIENDLY.get(rule_id)
    if not explanation:
        explanation = f"Review the {service or 'cloud'} configuration to restrict access permissions: {title}."

    return {
        "explanation": explanation,
        "danger": "This issue should be fixed before attackers can take advantage of it.",
        "real_world_impact": "Leaving the issue open can expose cloud resources, data, or credentials.",
        "remediation_steps": steps,
        "estimated_effort": "Easy (5-15 minutes)",
    }


def _generic_steps(service: str, title: str) -> List[str]:
    return [
        f"Review the {service or 'cloud'} finding carefully.",
        "Tighten access to the smallest set of users, ports, or resources needed.",
        f"Re-test the issue after fixing: {title or 'the rule'}",
    ]