import sys
import boto3
import json
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, when, round
from pyspark.sql.types import TimestampType

# Argumentos de entrada (pasados desde Lambda)
args = sys.argv
input_bucket = args[args.index("--input_bucket") + 1]
input_key = args[args.index("--input_key") + 1]

# Iniciar Spark Session
spark = SparkSession.builder.appName("ETL-S3-to-Snowflake-pleasure").getOrCreate()

# Construir la ruta completa del archivo en S3
s3_path = f"s3://{input_bucket}/{input_key}"

# Obtener el nombre base del archivo sin extensión
input_filename = os.path.basename(input_key)
output_filename = os.path.splitext(input_filename)[0] + ".parquet"

# Leer archivo JSON desde S3
df = spark.read.json(s3_path)

# 🔍 Data Quality Checks - Field-specific constraints

# 1. Check for required fields (NOT NULL constraints)
required_fields = ["video_id", "chunk_start_time", "chunk_end_time", "view_date"]
for field in required_fields:
    # Count null values before filtering
    null_count = df.filter(col(field).isNull()).count()
    print(f"Found {null_count} null values in field {field}")
    
    # Filter out null values
    df = df.filter(col(field).isNotNull())

# 2. Validate video_id format (assuming it should be alphanumeric)
df = df.withColumn("video_id_valid", 
                  col("video_id").rlike("^[a-zA-Z0-9_-]+$"))
invalid_video_ids = df.filter(~col("video_id_valid")).select("video_id").distinct()
print(f"Found {invalid_video_ids.count()} invalid video_id formats")
df = df.filter(col("video_id_valid")).drop("video_id_valid")

# 3. Validate time chunks (chunk_start_time < chunk_end_time)
df = df.withColumn("time_chunk_valid", 
                  col("chunk_start_time") < col("chunk_end_time"))
invalid_time_chunks = df.filter(~col("time_chunk_valid")).count()
print(f"Found {invalid_time_chunks} records with invalid time chunks (start >= end)")
df = df.filter(col("time_chunk_valid")).drop("time_chunk_valid")

# 4. Add total_time field (chunk duration in seconds)
df = df.withColumn("total_time", 
                  round(col("chunk_end_time") - col("chunk_start_time"), 2))

# 5. Validate view_date format (assuming it should be a valid date)
try:
    df = df.withColumn("view_date_parsed", to_timestamp(col("view_date")))
    invalid_dates = df.filter(col("view_date_parsed").isNull()).count()
    print(f"Found {invalid_dates} invalid view_date formats")
    df = df.filter(col("view_date_parsed").isNotNull())
except Exception as e:
    print(f"Error parsing view_date: {str(e)}")
    raise

# 6. Validate timestamp (should not be in the future)
# Option 1: Convert your timestamp column to timestamp type (if it's Unix time in seconds)
df = df.withColumn("timestamp_converted", 
                  (col("timestamp").cast("timestamp")))

current_timestamp = spark.sql("SELECT current_timestamp()").collect()[0][0]
df = df.withColumn("timestamp_valid", 
                  (col("timestamp_converted") <= current_timestamp))
future_timestamps = df.filter(~col("timestamp_valid")).count()
print(f"Found {future_timestamps} records with timestamps in the future")
df = df.filter(col("timestamp_valid")).drop("timestamp_valid", "timestamp_converted")

# 7. Validate total_time (should be positive and reasonable)
df = df.withColumn("total_time_valid",
                  (col("total_time") > 0) & (col("total_time") <= 86400))  # Max 24 hours
invalid_durations = df.filter(~col("total_time_valid")).count()
print(f"Found {invalid_durations} records with invalid chunk durations")
df = df.filter(col("total_time_valid")).drop("total_time_valid")

# Guardar como Parquet en otra ubicación en S3, manteniendo el mismo nombre de archivo
output_path = f"s3://raspberry-pi-logs-bucket/output/{output_filename}"
df.write.mode("overwrite").parquet(output_path)

print(f"Datos limpios guardados en {output_path}")
print(f"Data quality checks completed. Final record count: {df.count()}")
print(f"Sample records with total_time calculation:")
df.select("video_id", "chunk_start_time", "chunk_end_time", "total_time").show(5)
