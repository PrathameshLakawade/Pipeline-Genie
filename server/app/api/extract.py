from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException, Request

from services.s3_service import upload_file, fetch_details
from services.database_service import insert_record, fetch_record, update_record
from services.spark_service import read_csv, get_details
from configuration.settings import settings

router = APIRouter()


# Upload file to the base layer
@router.post("/upload")
async def upload_to_base_layer(request: Request, files: List[UploadFile] = File(...)):
    try:
        for file in files:
            key = f"{settings.AWS_BASE_LAYER}/{file.filename}"
            if upload_file(request, file, settings.AWS_S3_BUCKET, key):
                metadata = {
                    "filename": file.filename,
                    "key": key,
                    "s3_uri": f"s3a://{settings.AWS_S3_BUCKET}/{key}",
                }
                
                if insert_record(request, metadata):
                    metadata["_id"] = str(metadata["_id"])
                return {"status": "success", "id": metadata["_id"]}
            else:
                return {"status": "failed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Generate metadata
@router.get("/metadata/{id}")
async def generate_metadata(request: Request, id: str):
    try:
        record = fetch_record(request, id)
        aws_metadata = fetch_details(request, settings.AWS_S3_BUCKET, record['key'])
        
        if read_csv(request, record['s3_uri']):
            rows, columns, data_types = get_details(request)

            metadata = {
                "size": aws_metadata['ContentLength'],
                "last_modified": aws_metadata['LastModified'],
                "rows": rows,
                "columns": columns,
                "data_types": data_types,
            }
        
            update_record(request, id, metadata)
            record = fetch_record(request, id)
            
            return {"status": "success", "id": record["_id"], "metadata": record}
        else:
            return {"status": "failed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        