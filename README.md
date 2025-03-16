---

## ✅ Pipeline Stages

### 1️⃣ Extract Logs
- Connect to S3 bucket.
- Download all `.log` files from the `raw-logs` folder.

### 2️⃣ Transform Logs
- Filter only lines with `ERROR` or `500` status codes.
- Store the filtered logs in-memory.

### 3️⃣ Load Logs
- Upload the filtered logs to the `processed-logs` folder in the same bucket.

---

## 🛠️ Technology Stack
- **Airflow DAGs** for pipeline coordination.
- **Python (Boto3)** for S3 interaction.
- **Docker** for Airflow environment.
- **GitHub Actions / GitLab CI/CD** for deployment.

---

## 🛠️ Installation Guide

### 1️⃣ Install Docker and Docker Compose
Ensure Docker is installed on your machine. If not, install it from [Docker Official Site](https://www.docker.com/).

### 2️⃣ Clone the Repository
```
git clone https://github.com/your-repo/my_s3_airflow_pipeline.git
cd my_s3_airflow_pipeline
```

### 3️⃣ Set up AWS Credentials
Configure your AWS credentials in `cloud/aws/s3_config.json`.

### 4️⃣ Start Airflow with Docker Compose
```
cd airflow
docker-compose up -d
```

### 5️⃣ Access Airflow UI
Visit `http://localhost:8080` and activate the DAG `s3_etl_pipeline`.

---

## 🚀 Deployment on Cloud

### 1️⃣ Deploy to AWS Managed Airflow
- Push the DAG to S3 bucket assigned to AWS Managed Airflow.

### 2️⃣ Deploy to Cloud Composer (GCP)
- Upload the DAG to the DAG bucket in Cloud Composer.

---

## 📈 Airflow DAG Code
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import boto3
import pandas as pd
import io

# AWS S3 Configuration
BUCKET_NAME = 'my-bucket'
RAW_LOGS_FOLDER = 'raw-logs/'
PROCESSED_LOGS_FOLDER = 'processed-logs/'