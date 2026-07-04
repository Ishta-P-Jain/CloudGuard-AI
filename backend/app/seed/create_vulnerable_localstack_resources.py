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

def seed_s3():
    print("Seeding S3 buckets...")
    
    # 1. Vulnerable public write access bucket
    bucket_name = "vulnerable-bucket-public-write"
    try:
        s3.create_bucket(Bucket=bucket_name)
        # Put public ACL
        s3.put_bucket_acl(Bucket=bucket_name, ACL="public-read-write")
        # Put public access block to ALLOW public (False)
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        print(f"Created bucket {bucket_name} with public read/write access.")
    except Exception as e:
        print(f"Bucket {bucket_name} could not be created or already exists: {e}")

    # 2. Vulnerable bucket missing encryption
    bucket_name = "vulnerable-bucket-missing-encryption"
    try:
        s3.create_bucket(Bucket=bucket_name)
        s3.put_bucket_acl(Bucket=bucket_name, ACL="private")
        print(f"Created bucket {bucket_name} with encryption disabled.")
    except Exception as e:
        print(f"Bucket {bucket_name} could not be created or already exists: {e}")

    # 3. Secure bucket with encryption
    bucket_name = "secure-bucket"
    try:
        s3.create_bucket(Bucket=bucket_name)
        s3.put_bucket_acl(Bucket=bucket_name, ACL="private")
        s3.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    }
                ]
            }
        )
        print(f"Created bucket {bucket_name} with AES256 encryption enabled.")
    except Exception as e:
        print(f"Bucket {bucket_name} could not be created or already exists: {e}")

def seed_iam():
    print("Seeding IAM users and policies...")
    
    # 1. Vulnerable IAM User (no MFA)
    user_name = "vulnerable-user-no-mfa"
    try:
        iam.create_user(UserName=user_name)
        print(f"Created IAM user {user_name} with no MFA.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"IAM user {user_name} already exists.")
    except Exception as e:
        print(f"Error creating user {user_name}: {e}")

    # 2. Secure IAM User (with MFA)
    user_name = "secure-user-mfa"
    try:
        iam.create_user(UserName=user_name)
        mfa_resp = iam.create_virtual_mfa_device(
            VirtualMFADeviceName="secure-user-mfa-device"
        )
        device_arn = mfa_resp["VirtualMFADevice"]["SerialNumber"]
        iam.enable_mfa_device(
            UserName=user_name,
            SerialNumber=device_arn,
            AuthenticationCode1="123456",
            AuthenticationCode2="789012"
        )
        print(f"Created IAM user {user_name} and enabled virtual MFA device.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"IAM user {user_name} or device already exists.")
    except Exception as e:
        print(f"Error creating user {user_name} with MFA: {e}")

    # Helper function to create policy
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

    # 3. Vulnerable Admin Policy (Allow * on *)
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

    # 4. Vulnerable Broad Policy (Allow s3:* on *)
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

    # 5. Secure Limited Policy (Allow s3:GetObject on specific resource)
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

def seed_ec2():
    print("Seeding EC2 Security Groups...")
    
    try:
        vpcs = ec2.describe_vpcs()
        vpc_id = vpcs["Vpcs"][0]["VpcId"]
    except Exception:
        vpc_id = None

    def create_security_group(name, desc):
        try:
            kwargs = {"GroupName": name, "Description": desc}
            if vpc_id:
                kwargs["VpcId"] = vpc_id
            sg = ec2.create_security_group(**kwargs)
            return sg["GroupId"]
        except Exception as e:
            try:
                sgs = ec2.describe_security_groups(GroupNames=[name])
                return sgs["SecurityGroups"][0]["GroupId"]
            except Exception:
                print(f"Error creating/fetching security group {name}: {e}")
                return None

    # 1. Vulnerable SSH Open (Port 22)
    sg_ssh = create_security_group("vulnerable-ssh-open", "Security group with open port 22")
    if sg_ssh:
        try:
            ec2.authorize_security_group_ingress(
                GroupId=sg_ssh,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )
            print(f"Authorized ingress on vulnerable-ssh-open (Port 22 from 0.0.0.0/0).")
        except Exception as e:
            print(f"Rule already exists or failed for vulnerable-ssh-open: {e}")

    # 2. Vulnerable RDP Open (Port 3389)
    sg_rdp = create_security_group("vulnerable-rdp-open", "Security group with open port 3389")
    if sg_rdp:
        try:
            ec2.authorize_security_group_ingress(
                GroupId=sg_rdp,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 3389,
                        'ToPort': 3389,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )
            print(f"Authorized ingress on vulnerable-rdp-open (Port 3389 from 0.0.0.0/0).")
        except Exception as e:
            print(f"Rule already exists or failed for vulnerable-rdp-open: {e}")

    # 3. Secure SG
    sg_secure = create_security_group("secure-sg", "Secure Security Group")
    if sg_secure:
        print("Created secure-sg security group.")

def main():
    seed_s3()
    seed_iam()
    seed_ec2()
    print("Seeding completed successfully! --- Done")

if __name__ == "__main__":
    main()
