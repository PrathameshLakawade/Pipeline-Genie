from fastapi import Request, UploadFile


# Upload file
def upload_file(request: Request, file: UploadFile, bucket_name: str, key: str):
    try:
        logger = request.app.state.logger
        s3_client = request.app.state.s3_client
        
        if not s3_client:
            raise Exception("AWS S3 client is not initialized!")
        
        s3_client.upload_fileobj(file.file, bucket_name, key)
        logger.info("File successfully uploaded!")
        
        return True
    except Exception as e:
        logger.error(f"Failed to upload file: {str(e)}")
        raise Exception(f"Failed to upload file: {str(e)}")


# Fetch file
def fetch_details(request: Request, bucket_name: str, key: str):
    try:
        logger = request.app.state.logger
        s3_client = request.app.state.s3_client
        
        if not s3_client:
            raise Exception("S3 client is not initialized!")
        
        response = s3_client.head_object(Bucket=bucket_name, Key=key)
        logger.info("Successfully fetched details!")

        return response
    except Exception as e:
        logger.error(f"Failed to fetch details: {str(e)}")
        raise Exception(f"Failed to fetch details: {str(e)}")


# Combine files
def combine_files(request: Request, bucket_name: str, key: str):
    try:
        logger = request.app.state.logger
        s3_client = request.app.state.s3_client
        
        if not s3_client:
            raise Exception("S3 client is not initialized!")

        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=f"{key}/")

        part_files = [obj["Key"] for obj in response.get("Contents", [])]

        if not part_files:
            raise Exception(f"No files found in folder '{key}/'")

        csv_parts = [file for file in part_files if "part-" in file]

        if not csv_parts:
            raise Exception(f"No part files found to combine in folder '{key}/'")

        final_file_key = key.rstrip("/")
        with open("/tmp/combined.csv", "wb") as combined_file:
            for part_file in csv_parts:
                obj = s3_client.get_object(Bucket=bucket_name, Key=part_file)
                combined_file.write(obj["Body"].read())

        with open("/tmp/combined.csv", "rb") as combined_file:
            s3_client.put_object(Bucket=bucket_name, Key=final_file_key, Body=combined_file)

        delete_objects = [{"Key": obj} for obj in part_files]
        s3_client.delete_objects(Bucket=bucket_name, Delete={"Objects": delete_objects})

        logger.info(f"Successfully combined part files into '{final_file_key}'.")
        return True

    except Exception as e:
        logger.error(f"Failed to combine partition files: {str(e)}")
        raise Exception(f"Failed to combine partition files: {str(e)}")


# Clone files
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


# List files
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
