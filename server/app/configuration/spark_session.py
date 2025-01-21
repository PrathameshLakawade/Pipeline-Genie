from fastapi import FastAPI
from pyspark.sql import SparkSession

from configuration.settings import settings

async def initialze_spark_session(app: FastAPI):
    try:
        logger = app.state.logger
        spark_session = SparkSession.builder \
            .appName(settings.SPARK_APPLICATION_NAME) \
            .config("spark.driver.memory", settings.SPARK_DRIVER_MEMORY) \
            .config("spark.executor.memory", settings.SPARK_EXECUTOR_MEMORY) \
            .config("spark.driver.bindAddress", "127.0.0.1") \
            .config("spark.driver.host", "localhost") \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
            .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
            .config("spark.hadoop.fs.s3a.access.key", settings.AWS_ACCESS_KEY_ID) \
            .config("spark.hadoop.fs.s3a.secret.key", settings.AWS_SECRET_ACCESS_KEY) \
            .getOrCreate()
        
        spark_session.sparkContext.setLogLevel("INFO")
        logger.info("Successfully initialized spark session!")
        
        return spark_session
    except Exception as e:
        logger.error(f"Failed to initialize spark session: {str(e)}")
        raise e