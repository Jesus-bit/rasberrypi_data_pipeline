from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count
from datetime import datetime
from boto3_client import s3_client  # 📌 Importar cliente S3 desde boto3_client.py

# Iniciar sesión en Spark
spark = SparkSession.builder.appName("VideoAnalytics").getOrCreate()

def get_s3_log_file():
    """Obtiene el archivo de logs del día actual desde S3."""
    s3_bucket = "video-logs"
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")
    file_name = f"video_log_{day}.log"
    s3_path = f"s3://{s3_bucket}/{year}/{month}/{file_name}"
    return s3_path

s3_file = get_s3_log_file()
# 📌 Leer logs desde S3
df = spark.read.option("header", True).csv(s3_file)

# 📌 Filtrar los eventos de "play" y calcular vistas por cada chunk de video
df_filtered = df.filter(col("event") == "play") \
                .groupBy("video_id", "chunk_id") \
                .agg(count("*").alias("views"))

# 📌 Guardar resultados en S3 (procesados)
output_path = f"s3://processed-data/video_chunks_{year}_{month}_{day}.csv"
df_filtered.write.mode("overwrite").csv(output_path)
print("✅ Datos procesados y guardados en S3")