from fastapi import Request

def insert_record(request: Request, metadata: dict):
    try:
        logger = request.app.state.logger
        
        metadata_collection = request.app.state.mongo_collection
        if metadata_collection is None:
            raise Exception("MongoDB collection is not initialized!")

        metadata_collection.insert_one(metadata)
        logger.info("Record inserted successfully!")
        
        return True
    except Exception as e:
        logger.error(f"Failed to insert record: {str(e)}")
        raise Exception(f"Failed to insert record: {str(e)}")