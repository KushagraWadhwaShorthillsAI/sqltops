import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="rootpassword",
    database="demo_mysql",
    auth_plugin="caching_sha2_password",
    use_pure=True,
    ssl_disabled=True
)

print("Python MySQL connection OK")
conn.close()
