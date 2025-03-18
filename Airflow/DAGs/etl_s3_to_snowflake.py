from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import subprocess

def run_pyspark():
    """Ejecuta el script de PySpark."""
    subprocess.run(["spark-submit", "pyspark_etl/process_videos.py"])

def upload_to_snowflake():
    """Ejecuta el script para subir los datos a Snowflake."""
    subprocess.run(["python3", "airflow/dags/upload_snowflake.py"])

# Definir DAG
dag = DAG(
    dag_id="etl_s3_to_snowflake",
    schedule_interval="@daily",
    start_date=datetime(2025, 3, 17),
    catchup=False
)

# Tareas
task_pyspark = PythonOperator(
    task_id="run_pyspark",
    python_callable=run_pyspark,
    dag=dag
)

task_snowflake = PythonOperator(
    task_id="upload_snowflake",
    python_callable=upload_to_snowflake,
    dag=dag
)

# Flujo de ejecución
task_pyspark >> task_snowflake
