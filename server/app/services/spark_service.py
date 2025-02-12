from fastapi import Request
from pyspark.ml.feature import OneHotEncoder, StringIndexer
from pyspark.sql.functions import regexp_replace, explode, col


# Read CSV
def read_csv(request: Request, s3_uri: str):
    spark = request.app.state.spark_session
    
    df = spark.read.csv(s3_uri, inferSchema=True, header=True)
    request.app.state.dataframe = df
    
    return True


# Write CSV
def write_csv(request: Request, bucket_name: str, key: str):
    df = request.app.state.dataframe
    
    df.write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(f"s3a://{bucket_name}/{key}")
    
    return True


# Fetch DataFrame Details
def get_details(request: Request):
    df = request.app.state.dataframe
    rows = df.count()
    columns = df.columns
    data_types = {col: str(df.schema[col].dataType) for col in columns}
    
    return rows, columns, data_types


# Remove Null Values
def remove_null(request: Request):
    df = request.app.state.dataframe
    request.app.state.dataframe = df.dropna()
    
    return True


# Encode Categorical Data
def one_hot_encode(request: Request, columns):
    df = request.app.state.dataframe
    
    for column in columns:
        indexer = StringIndexer(inputCol = column, outputCol = column + "_index")
        encoder = OneHotEncoder(inputCol = column + "_index", outputCol = column + "_encoded")
        df = indexer.fit(df).transform(df)
        df = encoder.fit(df).transform(df)
        df = df.drop(column + "_index")
        
    return True


# Sanitize Text Fields
def sanitize_text(request: Request, columns):
    df = request.app.state.dataframe
    
    for column in columns:
        df = df.withColumn(column, regexp_replace(col(column), "[^a-zA-Z0-9 ]", ""))
    
    return True


# Explode Complex Columns
def explode_column(request: Request, columns):
    df = request.app.state.dataframe
    
    for column in columns:
        df = df.withColumn(column + "_exploded", explode(col(column)))
    
    return True