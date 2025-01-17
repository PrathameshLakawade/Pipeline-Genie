import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from core.config import settings
from core.logging import logger

# Global S3 client
s3_client = None

def connect_to_s3():
    global s3_client
    if not s3_client:
        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
            )
            buckets = s3_client.list_buckets()
            logger.info("S3 buckets: %s", [bucket["Name"] for bucket in buckets["Buckets"]])
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.error(f"Failed to connect to AWS S3: {str(e)}")
            raise e
    return s3_client
