# **Overview**
Pipeline-Genie is an intelligent data pipeline that processes CSV datasets, identifies their schema, and leverages LLaMA 2.0 to extract business insights. It allows users to choose relevant business needs and applies appropriate transformations using Apache Spark for efficient ETL. The final transformed dataset is stored and made available for download.

## **Tech Stack**
- **Frontend**: React
- **Backend**: FastAPI
- **Database**: MongoDB Atlas
- **AI Integration**: LLaMA 2.0
- **Storage**: AWS S3
- **ETL Processing**: Apache Spark

## **Features**
1. **CSV Upload**: User upload CSV files for processing.
2. **Schema Identification**: The system defects schema and null values in the dataset.
3. **AI-Powered Insights**: A sample of the dataset is fed to LLaMA 2.0, which suggests potential business insights.
4. **User Selection**: Users select relevant business needs from LLaMA's suggestions.
5. **Data Transformation**: The system applies necessary transformations such as:
    - Exploding object columns
    - Checking string columns for unknown characters
    - One-hot encoding categorical variables
    - Other relevant ETL processes
6. **Final CSV Generation**: A transformed CSV is generated and stored in AWS S3 for user download.

## **Screenshots & Visuals**
### CSV Upload
![CSV Upload][./docs/select-csv.png]

### Schema Detection
![Schema Detection][./docs/infer-schema.png]

### Business Insights
![Business Insights][./docs/business-need.png]

# **Installation & Setup**
## **Prerequisites**
- Python 3.8+
- Node.js 16+
- MongoDB Atlas Account
- AWS S3 bucket
- Apache Spark Setup

## **Backend Setup**
1. Clone the respository:
```
git clone https://github.com/your-repo/pipeline-genie.git
```
2. Create a virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r server/requirements.txt
```
3. Set up environment variables(Create `.env` file inside `server` folder):
```
# AWS Configuration
AWS_S3_BUCKET='your_aws_s3_bucket'
AWS_BASE_LAYER='your_base_layer_name'
AWS_INTERMEDIATE_LAYER='your_intermediate_layer_name'
AWS_FINAL_LAYER='your_final_layer_name'
AWS_ACCESS_KEY_ID='your_aws_access_key_id'
AWS_SECRET_ACCESS_KEY='your_aws_secret_access_key'
AWS_REGION='your_aws_region'

# MongoDB Configuration
MONGO_CLIENT='your_mongo_client_connection_uri'
MONGO_DATABASE='your_mongo_database_name'
MONGO_COLLECTION='your_mongo_collection_name'

# Logger Configuration
LOGGER_NAME='your_personalized_logger_name'
LOGGER_FORMAT='[%(asctime)s] %(levelname)s: %(message)s'

# Spark Configuration
SPARK_APPLICATION_NAME='your_personalized_spark_application_name'
SPARK_DRIVER_MEMORY='2g'
SPARK_EXECUTOR_MEMORY='2g'
```
4. Start the FastAPI backend:
```
cd server
uvicorn main:app --reload
```

## Frontend Setup
1. Navigate to the frontend directory:
```
cd ../client
```
2. Install dependencies:
```
npm install
```
3. Start the React app:
```
npm start
```

## Apache Spark Setup
Ensure Apache Spark is installed and configured correctly. Run Spark jobs as needed for ETL processing.

# Usage
1. Upload a CSV file via the frontend.
2. Let the system analyze the dataset and provide insights.
3. Select a relevant business need.
4. The system applies necessary transformations.
5. Download the transformed CSV file from AWS S3.

# Future Enhancements
- Support for additional file formats (JSON, Parquet)
- Advanced NLP-based insights using fine-tuned LLaMA models
- Real-time streaming support with Apache Kafka

# License
This project is licensed under the MIT Lincense.