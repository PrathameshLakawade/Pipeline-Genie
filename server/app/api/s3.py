from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from services.s3_service import upload_to_s3, remove_from_s3
from core.logging import logger

router = APIRouter()

@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    try:
        file_name = file.filename
        result = upload_to_s3(request, file, file_name)
        if result:
            logger.info("File Uploaded Successfully!")
            return {"status": "success"}
        else:
            return {"status": "failed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/remove/{file_name}")
async def remove_file(file_name: str):
    try:
        result = remove_from_s3(file_name)
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))