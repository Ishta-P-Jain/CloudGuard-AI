from app.cloud.localstack_client import iam

def list_users():
    """
    Returns a list of IAM user names.
    This is used to satisfy the Day 9 requirements.
    """
    try:
        response = iam.list_users()
        return [user["UserName"] for user in response.get("Users", [])]
    except Exception as e:
        print(f"Error listing IAM users: {e}")
        return []

def list_policies():
    """
    Returns a list of IAM policy names.
    This is used to satisfy the Day 9 requirements.
    """
    try:
        response = iam.list_policies(Scope="Local")
        return [policy["PolicyName"] for policy in response.get("Policies", [])]
    except Exception as e:
        print(f"Error listing IAM policies: {e}")
        return []

def collect_iam_resources():
    """
    Collects detailed IAM user and policy data for the rule engine.
    Returns:
        tuple: (users_list, policies_list)
    """
    users_data = []
    policies_data = []

    # 1. Collect Users and check MFA status
    user_names = list_users()
    for user_name in user_names:
        mfa_enabled = False
        try:
            mfa_resp = iam.list_mfa_devices(UserName=user_name)
            if mfa_resp.get("MFADevices"):
                mfa_enabled = True
        except Exception as e:
            print(f"Error checking MFA for user {user_name}: {e}")
        
        users_data.append({
            "user_name": user_name,
            "mfa_enabled": mfa_enabled
        })

    # 2. Collect Managed Policies and retrieve policy documents
    try:
        policies_resp = iam.list_policies(Scope="Local")
        for policy in policies_resp.get("Policies", []):
            policy_name = policy["PolicyName"]
            arn = policy["Arn"]
            default_version_id = policy.get("DefaultVersionId")
            
            policy_document = {}
            if default_version_id:
                try:
                    version_resp = iam.get_policy_version(PolicyArn=arn, VersionId=default_version_id)
                    policy_document = version_resp.get("PolicyVersion", {}).get("Document", {})
                except Exception as e:
                    print(f"Error getting policy version for {policy_name}: {e}")
            
            policies_data.append({
                "policy_name": policy_name,
                "policy_document": policy_document
            })
    except Exception as e:
        print(f"Error collecting IAM policies: {e}")

    return users_data, policies_data
