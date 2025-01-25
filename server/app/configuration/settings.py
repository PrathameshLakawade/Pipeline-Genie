import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # AWS Configuration
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    AWS_BASE_LAYER = os.getenv("AWS_BASE_LAYER")
    AWS_INTERMEDIATE_LAYER = os.getenv("AWS_INTERMEDIATE_LAYER")
    AWS_FINAL_LAYER = os.getenv("AWS_FINAL_LAYER")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    
    # MongoDB Atlas Configuration
    MONGO_CLIENT = os.getenv("MONGO_CLIENT")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
    
    # Logger Configuration
    LOGGER_NAME = os.getenv("LOGGER_NAME")
    LOGGER_FORMAT = os.getenv("LOGGER_FORMAT")
    
    # Spark Configuration
    SPARK_APPLICATION_NAME = os.getenv("SPARK_APPLICATION_NAME")
    SPARK_DRIVER_MEMORY = os.getenv("SPARK_DRIVER_MEMORY")
    SPARK_EXECUTOR_MEMORY = os.getenv("SPARK_EXECUTOR_MEMORY")

settings = Settings()