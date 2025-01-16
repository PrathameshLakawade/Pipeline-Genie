from fastapi import FastAPI
from app.api.data_pipeline import router as data_pipeline_router

app = FastAPI(title="Pipeline Genie")

# Include the router
app.include_router(data_pipeline_router, prefix="/pipeline", tags=["Pipeline"])

@app.get("/")
def root():
    return {"message": "Welcome to Pipeline Genie"}