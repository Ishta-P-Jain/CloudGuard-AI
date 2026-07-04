import sys
from app.cloud.localstack_client import collect_resources
from app.cloud.s3_client import list_buckets
from app.cloud.iam_client import list_users, list_policies
from app.cloud.ec2_client import list_security_groups

def main():
    print("=== CLOUDGUARD AI - WEEK 2 DIAGNOSTICS ===")
    
    print("\n--- Day 7: localstack_client.py Connection Check ---")
    try:
        res = collect_resources()
        print("✅ Backend connected to LocalStack successfully!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Ensure Docker Desktop is running and LocalStack is active (docker compose up).")
        sys.exit(1)

    print("\n--- Day 8: s3_client.py Buckets Listing ---")
    buckets = list_buckets()
    print(f"Buckets found: {buckets}")
    
    print("\n--- Day 9: iam_client.py Users & Policies Listing ---")
    users = list_users()
    policies = list_policies()
    print(f"IAM Users found: {users}")
    print(f"IAM Policies found: {policies}")

    print("\n--- Day 10: ec2_client.py Security Groups Listing ---")
    sgs = list_security_groups()
    print(f"EC2 Security Groups found: {len(sgs)}")
    for sg in sgs:
        print(f" - Group Name: {sg['GroupName']}, Ingress Rules/Permissions: {sg['IpPermissions']}")

if __name__ == "__main__":
    main()
