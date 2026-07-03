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