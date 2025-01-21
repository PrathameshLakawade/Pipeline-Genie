from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException, Request

from services.s3_service import upload_file, fetch_details
from configuration.settings import settings

router = APIRouter()


# Upload file to the bronze layer
@router.post("/upload")
async def upload_to_bronze(request: Request, files: List[UploadFile] = File(...)):
    try:
        for file in files:
            uploaded_file = upload_file(request, file, settings.AWS_S3_BUCKET, "bronze/")
            if uploaded_file:
                file_details = fetch_details(
                    request, uploaded_file.get("file_name"), 
                    settings.AWS_S3_BUCKET, 
                    uploaded_file.get("prefix")
                )
                if file_details:
                    return {"status": "success", "file_name": uploaded_file.get("file_name")}
                else:
                    return {"status": "failed"}
            else:
                return {"status": "failed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        