import boto3

LOCALSTACK_ENDPOINT = "http://localhost:4566"

session = boto3.Session(
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

s3 = session.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT
)

iam = session.client(
    "iam",
    endpoint_url=LOCALSTACK_ENDPOINT
)

ec2 = session.client(
    "ec2",
    endpoint_url=LOCALSTACK_ENDPOINT
)

def collect_resources():
    """
    Collects raw resource configurations from simulated AWS (LocalStack).
    Imports are done inside the function to prevent circular imports.
    """
    from app.cloud.s3_client import collect_s3_resources
    from app.cloud.iam_client import collect_iam_resources
    from app.cloud.ec2_client import collect_ec2_resources

    s3_buckets = collect_s3_resources()
    iam_users, iam_policies = collect_iam_resources()
    ec2_security_groups = collect_ec2_resources()

    return {
        "s3_buckets": s3_buckets,
        "iam_users": iam_users,
        "iam_policies": iam_policies,
        "ec2_security_groups": ec2_security_groups
    }