from core.s3_connection import s3_client
from core.logging import logger
from core.config import settings

def upload_to_s3(file, file_name: str, bucket_name: str = settings.AWS_S3_BUCKET):
    """
    Upload a file to S3.

    Args:
        file: In-memory file object (e.g., from FastAPI `UploadFile`).
        file_name: Name to save in S3.
        bucket_name: S3 bucket name.

    Returns:
        str: Success message.
    """
    try:
        if not s3_client:
            raise Exception("S3 client is not initialized!")

        s3_client.upload_fileobj(file.file, bucket_name, file_name)
        logger.info(f"File {file_name} successfully uploaded to bucket {bucket_name}.")
        return True
    except Exception as e:
        logger.error(f"Failed to upload file: {str(e)}")
        raise Exception(f"Failed to upload file: {str(e)}")


def remove_from_s3(file_name: str, bucket_name: str = settings.AWS_S3_BUCKET):
    """
    Remove a file from S3.

    Args:
        file_name: Name of the file to delete from S3.
        bucket_name: S3 bucket name.

    Returns:
        str: Success message.
    """
    try:
        if not s3_client:
            raise Exception("S3 client is not initialized!")

        s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        logger.info(f"File {file_name} successfully deleted from bucket {bucket_name}.")
        return True
    except Exception as e:
        logger.error(f"Failed to remove file: {str(e)}")
        raise Exception(f"Failed to remove file: {str(e)}")
