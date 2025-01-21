from fastapi import Request, UploadFile


# Upload file to AWS S3 bucket
def upload_file(request: Request, file: UploadFile, bucket_name: str, prefix: str):
    try:
        logger = request.app.state.logger
        s3_client = request.app.state.s3_client
        
        if not s3_client:
            raise Exception("AWS S3 client is not initialized!")

        file_name = file.filename
        
        s3_client.upload_fileobj(file.file, bucket_name, f"{prefix}{file_name}")
        logger.info("File successfully uploaded!")
        
        return {"file_name": file_name, "prefix": prefix, "s3_uri": f"s3://{prefix}{file_name}"}
    except Exception as e:
        logger.error(f"Failed to upload file: {str(e)}")
        raise Exception(f"Failed to upload file: {str(e)}")


# Fetch file details from AWS S3
def fetch_details(request: Request, file_name: str, bucket_name: str, prefix: str):
    try:
        logger = request.app.state.logger
        s3_client = request.app.state.s3_client
        
        if not s3_client:
            raise Exception("S3 client is not initialized!")
        
        response = s3_client.head_object(Bucket=bucket_name, Key=f"{prefix}{file_name}")
        logger.info("Successfully fetched details!")

        return response
    except Exception as e:
        logger.error(f"Failed to fetch details: {str(e)}")
        raise Exception(f"Failed to fetch details: {str(e)}")


def clone_file(request: Request, file_name: str, source_bucket_name: str, destination_bucket_name: str):
    try:
        logger = request.app.state.logger
        s3_client = request.app.state.s3_client
        
        if not s3_client:
            raise Exception("S3 client is not initialized!")
        
        s3_client.copy_object(CopySource={'Bucket': source_bucket_name, 'Key': file_name}, Bucket=destination_bucket_name, Key=f'bronze/{file_name}')
        logger.info("File successfully cloned to bronze layer!")
        
        return f'bronze/{file_name}'
    except Exception as e:
        logger.error(f"Failed to copy file: {str(e)}")
        raise Exception(f"Failed to copy file: {str(e)}")


def list_files(request: Request, bucket_name: str):
    try:
        logger = request.app.state.logger
        s3_client = request.app.state.s3_client
        
        if not s3_client:
            raise Exception("S3 client not initialized!")
        
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            files = [obj['Key'] for obj in response['Contents']]
            logger.info("Successfully fetched file names from external source!")
            return files
        else:
            logger.warn("No files found in external source!")
    except Exception as e:
        logger.error(f"Failed to fetch file names: {str(e)}")
        raise Exception(f"Failed to fetch file names: {str(e)}")
