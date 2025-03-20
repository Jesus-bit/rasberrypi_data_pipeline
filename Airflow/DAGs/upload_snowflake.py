import snowflake.connector
import pandas as pd

# Conectar a Snowflake
conn = snowflake.connector.connect(
    user="mi_usuario",
    password="mi_contraseña",
    account="mi_cuenta"
)

cur = conn.cursor()

# 📌 Leer datos desde S3
df = pd.read_csv("s3://processed-data/video_chunks.csv")

# 📌 Crear tabla si no existe
cur.execute("""
    CREATE TABLE IF NOT EXISTS video_analytics (
        video_id STRING,
        chunk_id INT,
        views INT
    )
""")

# 📌 Insertar datos en Snowflake
for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO video_analytics (video_id, chunk_id, views) VALUES (%s, %s, %s)",
        (row["video_id"], row["chunk_id"], row["views"])
    )

conn.commit()
cur.close()
conn.close()

print("✅ Datos subidos a Snowflake exitosamente")
