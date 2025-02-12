from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, List

from services.s3_service import combine_files
from services.database_service import fetch_record, update_record
from services.spark_service import get_details, remove_null, one_hot_encode, sanitize_text, explode_column, write_csv
from services.llama_service import generate_business_needs
from configuration.settings import settings

router = APIRouter()


@router.post("/clean/{id}")
async def clean_data(request: Request, id: str):
    try:
        record = fetch_record(request, id)
        key = f"{settings.AWS_INTERMEDIATE_LAYER}/{record["filename"]}"
        
        remove_null(request)
        if write_csv(request, settings.AWS_S3_BUCKET, key):
            rows, columns, data_types = get_details(request)
            
            combine_files(request, settings.AWS_S3_BUCKET, key)
            
            record = fetch_record(request, id)
            response = generate_business_needs(request, rows, columns)
            
            metadata = {
                "key": key,
                "s3_uri": f"s3a://{settings.AWS_S3_BUCKET}/{key}",
                "rows": rows,
                "columns": columns,
                "data_types": data_types,
                "business_needs": response["business_needs"],
            }
            update_record(request, id, metadata)
        return {"status": "success", "id": record["_id"], "metadata": record, "response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class BusinessNeedRequest(BaseModel):
    id: str
    business_need: str
    transformations: Dict[str, List[str]]

    
@router.post("/process-business-need")
async def process_business_need(request1: Request, request: BusinessNeedRequest):
    try:
        logger = request1.app.state.logger
        logger.info(request.transformations)

        return {"message": "Business need received successfully!", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing business need: {str(e)}")