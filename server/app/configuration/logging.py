import logging

from configuration.settings import settings

async def initialize_logger():
    logging.basicConfig(level=logging.INFO, format=settings.LOGGER_FORMAT)
    logger = logging.getLogger(settings.LOGGER_NAME)
    logger.info("Successfully initialized logger!")
    
    return logger
