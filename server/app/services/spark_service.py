from fastapi import Request


# Read CSV
def read_csv(request: Request, s3_uri: str):
    spark = request.app.state.spark_session
    
    df = spark.read.csv(s3_uri, inferSchema=True, header=True)
    request.app.state.dataframe = df
    
    return True


# Get details
def get_details(request: Request):
    df = request.app.state.dataframe
    
    rows = df.count()
    columns = df.columns
    data_types = {col: str(df.schema[col].dataType) for col in columns}
    
    return rows, columns, data_types


# Clean dataframe
def remove_null(request: Request):
    df = request.app.state.dataframe
    
    request.app.state.dataframe = df.dropna()
    
    return True
    

# Write CSV
def write_csv(request: Request, bucket_name: str, key: str):
    df = request.app.state.dataframe
    
    df.write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(f"s3a://{bucket_name}/{key}")
    
    return True