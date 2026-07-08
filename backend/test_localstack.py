from app.cloud.localstack_client import s3

response = s3.list_buckets()

print(response)