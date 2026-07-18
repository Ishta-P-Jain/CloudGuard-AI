import argparse
import json
import boto3

LOCALSTACK_ENDPOINT = "http://localhost:4566"

session = boto3.Session(
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

s3 = session.client("s3", endpoint_url=LOCALSTACK_ENDPOINT)
iam = session.client("iam", endpoint_url=LOCALSTACK_ENDPOINT)
ec2 = session.client("ec2", endpoint_url=LOCALSTACK_ENDPOINT)


def create_bucket(bucket_name, acl="private", public_access_block=None, encryption=False):
    try:
        s3.create_bucket(Bucket=bucket_name)
    except Exception as e:
        print(f"Bucket {bucket_name} could not be created or already exists: {e}")

    try:
        s3.put_bucket_acl(Bucket=bucket_name, ACL=acl)
    except Exception as e:
        print(f"Could not set ACL for {bucket_name}: {e}")

    if public_access_block is not None:
        try:
            s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration=public_access_block
            )
        except Exception as e:
            print(f"Could not set public access block for {bucket_name}: {e}")

    if encryption:
        try:
            s3.put_bucket_encryption(
                Bucket=bucket_name,
                ServerSideEncryptionConfiguration={
                    "Rules": [
                        {
                            "ApplyServerSideEncryptionByDefault": {
                                "SSEAlgorithm": "AES256"
                            }
                        }
                    ]
                }
            )
        except Exception as e:
            print(f"Could not set encryption for {bucket_name}: {e}")


def create_user(user_name, enable_mfa=False):
    try:
        iam.create_user(UserName=user_name)
        print(f"Created IAM user {user_name}.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"IAM user {user_name} already exists.")
    except Exception as e:
        print(f"Error creating user {user_name}: {e}")

    if enable_mfa:
        try:
            mfa_resp = iam.create_virtual_mfa_device(
                VirtualMFADeviceName=f"{user_name}-device"
            )
            device_arn = mfa_resp["VirtualMFADevice"]["SerialNumber"]
            iam.enable_mfa_device(
                UserName=user_name,
                SerialNumber=device_arn,
                AuthenticationCode1="123456",
                AuthenticationCode2="789012"
            )
            print(f"Enabled MFA for {user_name}.")
        except Exception as e:
            print(f"Error enabling MFA for {user_name}: {e}")


def create_policy(policy_name, doc):
    try:
        iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(doc)
        )
        print(f"Created IAM policy {policy_name}.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"IAM policy {policy_name} already exists.")
    except Exception as e:
        print(f"Error creating policy {policy_name}: {e}")


def attach_policy_to_user(user_name, policy_arn):
    try:
        iam.attach_user_policy(
            UserName=user_name,
            PolicyArn=policy_arn
        )
        print(f"Attached policy to user {user_name}.")
    except Exception as e:
        print(f"Error attaching policy to {user_name}: {e}")


def create_security_group(name, desc):
    try:
        vpcs = ec2.describe_vpcs()
        vpc_id = vpcs["Vpcs"][0]["VpcId"] if vpcs.get("Vpcs") else None
    except Exception:
        vpc_id = None

    try:
        kwargs = {"GroupName": name, "Description": desc}
        if vpc_id:
            kwargs["VpcId"] = vpc_id
        sg = ec2.create_security_group(**kwargs)
        return sg["GroupId"]
    except Exception:
        try:
            sgs = ec2.describe_security_groups(GroupNames=[name])
            return sgs["SecurityGroups"][0]["GroupId"]
        except Exception as e:
            print(f"Error creating/fetching security group {name}: {e}")
            return None


def open_port(sg_id, port):
    try:
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                }
            ]
        )
        print(f"Opened port {port} on {sg_id}.")
    except Exception as e:
        print(f"Could not open port {port} on {sg_id}: {e}")


def seed_s3_safe():
    print("Seeding SAFE S3 resources...")
    create_bucket(
        "secure-bucket",
        acl="private",
        public_access_block={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True
        },
        encryption=True
    )


def seed_s3_mixed():
    print("Seeding MIXED S3 resources...")
    create_bucket(
        "vulnerable-bucket-public-write",
        acl="public-read-write",
        public_access_block={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False
        },
        encryption=False
    )
    create_bucket(
        "secure-bucket",
        acl="private",
        public_access_block={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True
        },
        encryption=True
    )


def seed_s3_risky():
    print("Seeding RISKY S3 resources...")
    create_bucket(
        "vulnerable-bucket-public-write",
        acl="public-read-write",
        public_access_block={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False
        },
        encryption=False
    )
    create_bucket(
        "vulnerable-bucket-missing-encryption",
        acl="private",
        public_access_block={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True
        },
        encryption=False
    )


def seed_iam_safe():
    print("Seeding SAFE IAM resources...")
    create_user("secure-user-mfa", enable_mfa=True)

    secure_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": "arn:aws:s3:::secure-bucket/*"
            }
        ]
    }
    create_policy("secure-limited-policy", secure_doc)


def seed_iam_mixed():
    print("Seeding MIXED IAM resources...")
    create_user("vulnerable-user-no-mfa", enable_mfa=False)
    create_user("secure-user-mfa", enable_mfa=True)

    broad_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": "*"
            }
        ]
    }
    create_policy("vulnerable-broad-policy", broad_doc)

    secure_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": "arn:aws:s3:::secure-bucket/*"
            }
        ]
    }
    create_policy("secure-limited-policy", secure_doc)


def seed_iam_risky():
    print("Seeding RISKY IAM resources...")
    create_user("vulnerable-user-no-mfa", enable_mfa=False)

    admin_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "*",
                "Resource": "*"
            }
        ]
    }
    create_policy("vulnerable-admin-policy", admin_doc)

    broad_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": "*"
            }
        ]
    }
    create_policy("vulnerable-broad-policy", broad_doc)


def seed_ec2_safe():
    print("Seeding SAFE EC2 resources...")
    sg_secure = create_security_group("secure-sg", "Secure Security Group")
    if sg_secure:
        print("Created secure-sg security group.")


def seed_ec2_mixed():
    print("Seeding MIXED EC2 resources...")
    sg_ssh = create_security_group("vulnerable-ssh-open", "Security group with open port 22")
    if sg_ssh:
        open_port(sg_ssh, 22)

    sg_secure = create_security_group("secure-sg", "Secure Security Group")
    if sg_secure:
        print("Created secure-sg security group.")


def seed_ec2_risky():
    print("Seeding RISKY EC2 resources...")
    sg_ssh = create_security_group("vulnerable-ssh-open", "Security group with open port 22")
    if sg_ssh:
        open_port(sg_ssh, 22)

    sg_rdp = create_security_group("vulnerable-rdp-open", "Security group with open port 3389")
    if sg_rdp:
        open_port(sg_rdp, 3389)

    sg_secure = create_security_group("secure-sg", "Secure Security Group")
    if sg_secure:
        print("Created secure-sg security group.")


def seed_profile(profile):
    profile = profile.lower()

    if profile == "safe":
        seed_s3_safe()
        seed_iam_safe()
        seed_ec2_safe()
    elif profile == "mixed":
        seed_s3_mixed()
        seed_iam_mixed()
        seed_ec2_mixed()
    elif profile == "risky":
        seed_s3_risky()
        seed_iam_risky()
        seed_ec2_risky()
    else:
        raise ValueError("Profile must be one of: safe, mixed, risky")


def main():
    parser = argparse.ArgumentParser(description="Seed LocalStack with different security scenarios.")
    parser.add_argument(
        "--profile",
        default="mixed",
        choices=["safe", "mixed", "risky"],
        help="Choose which resource profile to seed."
    )
    args = parser.parse_args()

    seed_profile(args.profile)
    print(f"Seeding completed successfully for profile: {args.profile}")


if __name__ == "__main__":
    main()