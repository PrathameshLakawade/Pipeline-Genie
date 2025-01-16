import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/pipeline_genie")
    S3_BUCKET = os.getenv("S3_BUCKET", "your-bucket-name")
    GEN_AI_API_KEY = os.getenv("GEN_AI_API_KEY", "your-api-key")

settings = Settings()