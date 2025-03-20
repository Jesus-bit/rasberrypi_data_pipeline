# 📌 Video Analytics System with Raspberry Pi, FastAPI, Airflow, PySpark, and Snowflake

## 📝 Description
This project is a complete video analytics system that:
- **Caches videos on a Raspberry Pi** for a single user.
- **Logs user interactions** and uploads them daily to an S3 bucket.
- **Triggers Airflow DAGs** when no login is detected for a set number of days.
- **Runs PySpark ETL** to process the logs.
- **Stores processed data in Snowflake** for AI training and analytics.

## 🏗️ Architecture
```
 User ↔ Raspberry Pi (Cache) ↔ FastAPI Backend → S3 (Logs) → Airflow (Trigger) → PySpark (ETL) → S3 (Processed Data) → Snowflake
```

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/video-analytics-system.git
cd video-analytics-system
```

### 2️⃣ Set Up the Raspberry Pi Cache
Install **FastAPI** on the Raspberry Pi:
```bash
pip install fastapi uvicorn boto3
```
Start the backend:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 3️⃣ Configure S3 Bucket
Create an S3 bucket and update your `.env` file:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET=your_bucket_name
```

### 4️⃣ Set Up Airflow
Install Airflow and dependencies:
```bash
pip install apache-airflow boto3 snowflake-connector-python
```
Start Airflow:
```bash
airflow db init
airflow scheduler & airflow webserver
```

### 5️⃣ Deploy PySpark
Install dependencies and run Spark jobs:
```bash
pip install pyspark
spark-submit pyspark_etl/process_videos.py
```

### 6️⃣ Set Up Snowflake Connection
Update `airflow/dags/upload_snowflake.py` with:
```
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
```

## 📌 Data Flow
1. **Raspberry Pi** caches videos & logs interactions.
2. **Logs are sent to S3** daily.
3. **Airflow triggers PySpark ETL** if no login is detected.
4. **PySpark processes logs** and stores results in S3.
5. **Processed data is uploaded to Snowflake**.
6. **AI models are trained using Snowflake data**.

## 🏃 Running the System
- **Start Raspberry Pi backend**: `uvicorn backend.main:app --reload`
- **Manually run the ETL**:
  ```bash
  airflow dags trigger etl_s3_to_snowflake
  ```
- **Run PySpark locally**:
  ```bash
  spark-submit pyspark_etl/process_videos.py
  ```

## 🛠️ TODO
- Automate AI training based on Snowflake data.
- Optimize costs by scheduling Airflow runs efficiently.
