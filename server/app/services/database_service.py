from fastapi import Request
from bson.objectid import ObjectId


# Insert a record
def insert_record(request: Request, record: dict):
    try:
        logger = request.app.state.logger
        
        metadata_collection = request.app.state.mongo_collection
        if metadata_collection is None:
            raise Exception("MongoDB collection is not initialized!")

        metadata_collection.insert_one(record)
        logger.info("Record inserted successfully!")
        
        return True
    except Exception as e:
        logger.error(f"Failed to insert record: {str(e)}")
        raise Exception(f"Failed to insert record: {str(e)}")
    

# Fetch a record using id
def fetch_record(request: Request, id: str):
    try:
        logger = request.app.state.logger
        
        metadata_collection = request.app.state.mongo_collection
        if metadata_collection is None:
            raise Exception("MongoDB collection is not initialized!")
        
        record = metadata_collection.find_one({"_id": ObjectId(id)})
        if record:
            if '_id' in record and isinstance(record['_id'], ObjectId):
                record['_id'] = str(record['_id'])
            
            logger.info("Record fetched successfully!")
            
            return record
    except Exception as e:
        logger.error(f"Failed to fetch record: {str(e)}")
        raise Exception(f"Failed to fetch record: {str(e)}")
    

# Update a record using id
def update_record(request: Request, id: str, record: dict):
    try:
        logger = request.app.state.logger
        
        metadata_collection = request.app.state.mongo_collection
        if metadata_collection is None:
            raise Exception("MongoDB collection is not initialized!")
        
        result = metadata_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": record}
        )
        
        if result.matched_count > 0:
            if result.modified_count > 0:
                logger.info("Record updated successfully!")
            else:
                logger.info("Record was not updated; the record is already updated!")
        else:
            logger.error("Record not found!")
    except Exception as e:
        logger.error(f"Failed to update record: {str(e)}")
        raise Exception(f"Failed to update record: {str(e)}")