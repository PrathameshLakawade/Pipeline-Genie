import boto3
from fastapi import FastAPI
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from configuration.settings import settings

async def initialize_s3_connection(app: FastAPI):
    try:
        logger = app.state.logger
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        buckets = s3_client.list_buckets()
        for bucket in buckets["Buckets"]:
            if bucket["Name"] == settings.AWS_S3_BUCKET:
                logger.info("Successfully initialized AWS S3 connection!")
                
                return s3_client
                
        logger.error("Failed to initialize S3 connection as bucket name did not match")
        return None
    except (NoCredentialsError, PartialCredentialsError) as e:
        logger.error(f"Failed to initialize S3 connection: {str(e)}")
        raise e
