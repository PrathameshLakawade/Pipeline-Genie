from fastapi import APIRouter, HTTPException
from app.services.data_pipeline_service import process_data, fetch_pipeline_status

router = APIRouter()

@router.post("/process")
def start_pipeline(file_path: str):
    try:
        result = process_data(file_path)
        return {"status": "success", "details": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
def pipeline_status(pipeline_id: str):
    try:
        status = fetch_pipeline_status(pipeline_id)
        return {"pipeline_id": pipeline_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
