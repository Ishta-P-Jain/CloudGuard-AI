from app.cloud.localstack_client import s3

def list_buckets():
    """
    Returns a simple list of bucket names.
    This is used to satisfy the Day 8 test requirements.
    """
    try:
        response = s3.list_buckets()
        return [bucket["Name"] for bucket in response.get("Buckets", [])]
    except Exception as e:
        print(f"Error listing S3 buckets: {e}")
        return []

def collect_s3_resources():
    """
    Collects detailed configuration of S3 buckets (ACLs, Encryption, Public Access).
    This is used by the rule engine to identify misconfigurations.
    """
    buckets_data = []
    bucket_names = list_buckets()
    
    for bucket_name in bucket_names:
        # 1. Check Public Access Block config
        public_access = False
        try:
            pab = s3.get_public_access_block(Bucket=bucket_name)
            pab_config = pab.get("PublicAccessBlockConfiguration", {})
            # If public policy or public ACL block is set to False (or not present), it is public
            if not pab_config.get("BlockPublicAcls", True) or not pab_config.get("BlockPublicPolicy", True):
                public_access = True
        except Exception:
            # If get_public_access_block fails (e.g. not configured), it defaults to public
            public_access = True

        # 2. Check ACL
        public_write_access = False
        acl_value = "private"
        try:
            acl_resp = s3.get_bucket_acl(Bucket=bucket_name)
            grants = acl_resp.get("Grants", [])
            for grant in grants:
                grantee = grant.get("Grantee", {})
                uri = grantee.get("URI", "")
                permission = grant.get("Permission", "")
                
                # Check if grant is for "All Users" (public)
                if "AllUsers" in uri:
                    if permission in ("READ", "FULL_CONTROL"):
                        public_access = True
                    if permission in ("WRITE", "WRITE_ACP", "FULL_CONTROL"):
                        public_write_access = True
                        acl_value = "public-read-write"
        except Exception:
            pass

        # 3. Check Server-Side Encryption
        encryption_enabled = False
        try:
            enc = s3.get_bucket_encryption(Bucket=bucket_name)
            rules = enc.get("ServerSideEncryptionConfiguration", {}).get("Rules", [])
            if rules:
                encryption_enabled = True
        except Exception:
            # If not configured, ServerSideEncryptionConfigurationNotFoundError is raised
            encryption_enabled = False

        buckets_data.append({
            "bucket_name": bucket_name,
            "public_access": public_access,
            "public_write_access": public_write_access,
            "acl": acl_value,
            "encryption_enabled": encryption_enabled
        })

    return buckets_data