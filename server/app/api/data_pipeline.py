from fastapi import APIRouter, HTTPException, Request

from services.s3_service import fetch_details
from services.database_service import insert_record
from configuration.settings import settings

router = APIRouter()

@router.get("/metadata/{file_name}")
async def generate_metadata(request: Request, file_name: str):
    try:
        aws_metadata = fetch_details(request, file_name, settings.AWS_S3_BUCKET, 'bronze/')
        
        spark = request.app.state.spark_session
        
        df = spark.read.csv(f"s3a://{settings.AWS_S3_BUCKET}/bronze/{file_name}", inferSchema=True, header=True)
        
        row_count = df.count()
        columns = df.columns
        data_types = {col: str(df.schema[col].dataType) for col in columns}
        
        metadata = {
            "file_path": f"s3://{settings.AWS_S3_BUCKET}/bronze/{file_name}",
            "file_size": aws_metadata['ContentLength'],
            "last_modified": aws_metadata['LastModified'],
            "row_count": row_count,
            "columns": columns,
            "data_types": data_types,
        }
        
        if insert_record(request, metadata):
            metadata["_id"] = str(metadata["_id"])
            return {"status": "success", "metadata": metadata}
        else:
            return {"status": "failed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/clean/{file_name}")
async def clean_data(request: Request, file_name: str):
    try:
        spark = request.app.state.spark_session
        
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))