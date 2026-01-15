import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="shtlpmac027",
    dbname="demo_postgres",
)

print("PostgreSQL connection OK")
conn.close()
