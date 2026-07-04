from app.cloud.localstack_client import ec2

def list_security_groups():
    """
    Returns a list of EC2 security groups with their GroupName and IpPermissions.
    This is used to satisfy the Day 10 requirements.
    """
    try:
        response = ec2.describe_security_groups()
        security_groups = []
        for sg in response.get("SecurityGroups", []):
            security_groups.append({
                "GroupId": sg.get("GroupId"),
                "GroupName": sg.get("GroupName"),
                "IpPermissions": sg.get("IpPermissions", [])
            })
        return security_groups
    except Exception as e:
        print(f"Error describing security groups: {e}")
        return []

def collect_ec2_resources():
    """
    Collects EC2 security group configurations for the rule engine.
    """
    return list_security_groups()
