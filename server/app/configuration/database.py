from pymongo import MongoClient
from fastapi import FastAPI

from configuration.settings import settings

async def initialize_database_connection(app: FastAPI):
    try:
        logger = app.state.logger
        mongo_client = MongoClient(settings.MONGO_CLIENT)
        mongo_database = mongo_client[settings.MONGO_DATABASE]
        mongo_collection = mongo_database[settings.MONGO_COLLECTION]
        logger.info("Successfully initialized database connection!")
        
        return mongo_collection
    except Exception as e:
        logger.error(f"Failed to initialize database connection: {str(e)}")