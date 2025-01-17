from fastapi import FastAPI
from api.s3 import router as s3_router
from core.s3_connection import connect_to_s3
from core.logging import logger


def app_factory() -> FastAPI:
    async def lifespan(app: FastAPI):
        logger.info("Starting up the application...")
        try:
            connect_to_s3()
            logger.info("S3 client successfully initialized during startup.")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {str(e)}")
            raise e

        yield

        logger.info("Shutting down the application...")

    app = FastAPI(title="Pipeline Genie", lifespan=lifespan)

    app.include_router(s3_router, prefix="/s3", tags=["S3"])

    @app.get("/")
    def root():
        return {"message": "Welcome to Pipeline Genie"}

    return app

app = app_factory()