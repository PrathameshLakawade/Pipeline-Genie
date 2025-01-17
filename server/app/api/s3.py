from fastapi import APIRouter, UploadFile, HTTPException
from services.s3_service import upload_to_s3, remove_from_s3

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile):
    try:
        file_name = file.filename
        result = upload_to_s3(file, file_name)
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/remove/{file_name}")
async def remove_file(file_name: str):
    try:
        result = remove_from_s3(file_name)
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/test")
def get_text():
    return {"status": "success", "message": "hello there"}