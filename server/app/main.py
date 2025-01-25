from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configuration.logging import initialize_logger
from configuration.s3_connection import initialize_s3_connection
from configuration.spark_session import initialze_spark_session
from configuration.database import initialize_database_connection

from api.extract import router as extract_router
from api.transform import router as transform_router


def app_factory() -> FastAPI:
    async def lifespan(app: FastAPI):
        app.state.logger = await initialize_logger()
        logger = app.state.logger
        
        logger.info("Starting Pipeline Genie Application!")
        
        app.state.s3_client = await initialize_s3_connection(app)
        app.state.spark_session = await initialze_spark_session(app)
        app.state.mongo_collection = await initialize_database_connection(app)

        yield

        logger.info("Shutting Down Pipeline Genie Application!")
        
        if app.state.spark_session:
            logger.info("Stopping Spark session...")
            app.state.spark_session.stop()
            logger.info("Spark session stopped successfully.")

    app = FastAPI(title="Pipeline Genie", lifespan=lifespan)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(extract_router, prefix="/extract", tags=["Extract"])
    app.include_router(transform_router, prefix="/transform", tags=["Transform"])


    @app.get("/")
    def root():
        return {"message": "Welcome to Pipeline Genie!"}

    return app

app = app_factory()