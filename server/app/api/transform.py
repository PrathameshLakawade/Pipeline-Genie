from fastapi import APIRouter, HTTPException, Request

from services.s3_service import combine_files
from services.database_service import fetch_record, update_record
from services.spark_service import get_details, remove_null, write_csv
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
            metadata = {
                "key": key,
                "s3_uri": f"s3a://{settings.AWS_S3_BUCKET}/{key}",
                "rows": rows,
                "columns": columns,
                "data_types": data_types,
            }
        update_record(request, id, metadata)
        combine_files(request, settings.AWS_S3_BUCKET, key)
        
        record = fetch_record(request, id)
        return {"status": "success", "id": record["_id"], "metadata": record}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))