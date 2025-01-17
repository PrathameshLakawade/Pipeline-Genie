# from fastapi import APIRouter, HTTPException
# from services.data_pipeline_service import upload_to_s3

# router = APIRouter()

# @router.post("/upload-raw-data")
# def upload_raw_data(file_path: str):
#     try:
#         result = upload_to_s3(file_path)
#         return {"status": "success", "message": result}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
