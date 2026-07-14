import os
import json
import requests
from typing import Any, Dict

# Groq API endpoint
GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
# Using a fast and cost-effective model on Groq
GROQ_MODEL = "llama3-8b-8192"

# High-quality rule-based fallback explanations and remediation steps
FALLBACK_EXPLANATIONS: Dict[str, Dict[str, Any]] = {
    "S3_PUBLIC_BUCKET_ACCESS": {
        "explanation": "This S3 bucket is configured with public read access, allowing anyone on the internet to list and read objects stored in it.",
        "danger": "Exposure of sensitive data (credentials, customer lists, logs, or source code) to unauthorized actors.",
        "real_world_impact": "Data leak leading to regulatory fines, reputational damage, and potential target for further exploits.",
        "remediation_steps": [
            "Open the AWS Console and go to S3.",
            "Select the public bucket and choose the 'Permissions' tab.",
            "Edit 'Block public access (bucket settings)' and check 'Block all public access'.",
            "Update the bucket policy to restrict Access Control Lists (ACLs)."
        ],
        "estimated_effort": "Easy (3 minutes)"
    },
    "S3_PUBLIC_WRITE_ACCESS": {
        "explanation": "This S3 bucket allows anyone on the internet to write, modify, or delete objects within it.",
        "danger": "Attackers can upload malicious scripts, overwrite critical assets, or use your bucket for hosting illegal files.",
        "real_world_impact": "Financial loss due to bandwidth abuse, site defacement, malware propagation, or ransomware attacks.",
        "remediation_steps": [
            "Navigate to the bucket permissions tab in the S3 console.",
            "Edit 'Access Control List (ACL)' settings.",
            "Remove 'Write' permissions granted to 'Everyone (public access)'.",
            "Enable 'Block all public access' settings for this bucket."
        ],
        "estimated_effort": "Easy (5 minutes)"
    },
    "S3_MISSING_ENCRYPTION": {
        "explanation": "This S3 bucket does not have Default Server-Side Encryption (SSE) enabled, meaning objects are stored in plaintext on disk.",
        "danger": "If the physical disks hosting the bucket are compromised, the stored data could be read directly.",
        "real_world_impact": "Failure to comply with industry compliance standards (like HIPAA, PCI-DSS, or GDPR) requiring encryption of data at rest.",
        "remediation_steps": [
            "Select the bucket in the S3 Console.",
            "Go to the 'Properties' tab.",
            "Scroll down to 'Default encryption' and click Edit.",
            "Select 'Enable' and choose encryption type (SSE-S3 or SSE-KMS)."
        ],
        "estimated_effort": "Easy (2 minutes)"
    },
    "IAM_MISSING_MFA": {
        "explanation": "This IAM user does not have Multi-Factor Authentication (MFA) enabled. Login depends solely on a username and password.",
        "danger": "If the user's password is stolen via phishing or credential stuffing, the attacker gets immediate console access.",
        "real_world_impact": "Account takeover leading to unauthorized creation of expensive resources, data deletion, or backdoors.",
        "remediation_steps": [
            "Log into the IAM console.",
            "Go to 'Users' and select the affected username.",
            "Choose the 'Security credentials' tab.",
            "Click 'Assign MFA device' and follow the setup instructions using an authenticator app or hardware token."
        ],
        "estimated_effort": "Medium (5 minutes)"
    },
    "IAM_OVERLY_PERMISSIVE_POLICY": {
        "explanation": "This IAM policy grants overly broad permissions (using wildcards like '*' on actions or resource scopes).",
        "danger": "Users or services attached to this policy have access to more resources and actions than they require, violating the Principle of Least Privilege.",
        "real_world_impact": "An compromised access key can be used by an attacker to delete databases, modify network settings, or access private logs.",
        "remediation_steps": [
            "Identify where this policy is attached (users, groups, or roles).",
            "Edit the policy JSON document.",
            "Replace wildcard permissions (e.g., 's3:*') with specific allowed actions (e.g., 's3:GetObject').",
            "Restrict the 'Resource' clause from '*' to specific ARNs."
        ],
        "estimated_effort": "Medium (15 minutes)"
    },
    "IAM_ADMIN_ACCESS_DETECTION": {
        "explanation": "This IAM policy grants full administrator privileges ('*' action on '*' resource), giving unrestricted control over the entire AWS account.",
        "danger": "This policy gives maximum access. If attached to non-admin entities, it poses a severe threat of complete account takeover.",
        "real_world_impact": "Unauthorized access to billing, resource deletion, credential hijacking, and malicious resource deployments.",
        "remediation_steps": [
            "Review the list of users or roles attached to this admin policy.",
            "Detached the policy from any entity that does not strictly require full admin rights.",
            "Replace it with standard managed power user or read-only policies where applicable."
        ],
        "estimated_effort": "Medium (10 minutes)"
    },
    "EC2_OPEN_SSH": {
        "explanation": "This security group allows inbound SSH traffic on TCP port 22 from any source (0.0.0.0/0).",
        "danger": "Exposes the virtual machine's command line to brute-force ssh login attempts from anywhere on the internet.",
        "real_world_impact": "Host takeover leading to server compromise, botnet enlistment, or lateral movement within your cloud network.",
        "remediation_steps": [
            "Open the EC2 console and navigate to 'Security Groups'.",
            "Select the security group and click 'Edit inbound rules'.",
            "Locate the rule for Port 22.",
            "Change the source from 'Anywhere-IPv4' (0.0.0.0/0) to 'My IP' or a specific secure bastion IP range."
        ],
        "estimated_effort": "Easy (3 minutes)"
    },
    "EC2_OPEN_RDP": {
        "explanation": "This security group allows inbound Remote Desktop Protocol (RDP) traffic on TCP port 3389 from any source (0.0.0.0/0).",
        "danger": "Exposes Windows remote desktop sessions to brute-force connection attempts and known Windows protocol exploits.",
        "real_world_impact": "Remote takeover of Windows servers, ransomware injection, and active directory compromise.",
        "remediation_steps": [
            "Go to the EC2 security group settings.",
            "Edit inbound rules and locate the rule for Port 3389.",
            "Restrict the source IP range to trusted client networks only."
        ],
        "estimated_effort": "Easy (3 minutes)"
    }
}

DEFAULT_FALLBACK = {
    "explanation": "This resource has a security misconfiguration that should be reviewed and remediated according to cloud security best practices.",
    "danger": "Potential exposure of resources or settings to unauthorized actors.",
    "real_world_impact": "Increased risk of compliance failure, data access, or resource compromise.",
    "remediation_steps": [
        "Inspect the security settings of this resource in the AWS Console.",
        "Apply the principle of least privilege to restrict access.",
        "Enable encryption and multi-factor authentication where applicable."
    ],
    "estimated_effort": "Medium (10 minutes)"
}

def explain_finding(finding: Dict[str, Any]) -> Dict[str, Any]:
    """
    Accepts a single finding dictionary and generates an AI-powered explanation.
    Queries Groq if GROQ_API_KEY environment variable is configured.
    Falls back to a high-quality static explanation if the API is offline or key is missing.
    """
    api_key = os.getenv("GROQ_API_KEY")
    rule_id = finding.get("rule_id", "")
    
    # 1. If API key is not present, return rule-based fallback immediately
    if not api_key:
        print(f"[AI Service] No GROQ_API_KEY found. Using rule-based fallback for {rule_id}.")
        return FALLBACK_EXPLANATIONS.get(rule_id, DEFAULT_FALLBACK)
        
    # 2. Prepare the prompt instructing the LLM to return JSON format matching response schema
    prompt = f"""
    You are a cloud security mentor explaining a finding to beginner engineering students.
    
    Finding Details:
    - Service: {finding.get('service', 'Unknown')}
    - Rule ID: {rule_id}
    - Resource: {finding.get('resource_id', 'Unknown')}
    - Severity: {finding.get('severity', 'Unknown')}
    - Description: {finding.get('description', 'No Description')}
    - Evidence: {json.dumps(finding.get('evidence', {}))}
    
    Please provide an analysis of this security finding.
    You MUST respond with a valid JSON object ONLY. Do not include any conversational preamble or markdown code fence blocks outside of the JSON.
    The JSON structure MUST contain the following keys exactly:
    1. "explanation": A simple plain-English explanation of what this finding means.
    2. "danger": The technical risks associated with leaving this unfixed.
    3. "real_world_impact": What could happen in a real company (e.g. data breach, fine, downtime).
    4. "remediation_steps": A list/array of 3-4 clear step-by-step instructions to fix this issue in AWS console.
    5. "estimated_effort": A short estimation of the effort to fix it (e.g., 'Easy (5 minutes)', 'Medium (15 minutes)').
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": application_json_headers() if hasattr(requests, "Session") else "application/json"
    }
    # Keep standard content-type header
    headers["Content-Type"] = "application/json"
    
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2
    }
    
    try:
        # Call Groq Chat Completion endpoint with a 10-second timeout
        response = requests.post(GROQ_API_ENDPOINT, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            resp_data = response.json()
            content = resp_data["choices"][0]["message"]["content"]
            parsed_json = json.loads(content)
            
            # Verify keys exist in the AI response
            required_keys = ["explanation", "danger", "real_world_impact", "remediation_steps", "estimated_effort"]
            if all(key in parsed_json for key in required_keys):
                return parsed_json
            else:
                print(f"[AI Service] LLM response was missing required keys. Fallback triggered.")
        else:
            print(f"[AI Service] API request failed with status {response.status_code}. Fallback triggered.")
            
    except Exception as e:
        print(f"[AI Service] Exception during API call: {e}. Fallback triggered.")
        
    # Return rule-based fallback as safe assurance
    return FALLBACK_EXPLANATIONS.get(rule_id, DEFAULT_FALLBACK)

def application_json_headers():
    return "application/json"
