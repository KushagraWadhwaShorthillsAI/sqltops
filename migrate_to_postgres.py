import mysql.connector
import psycopg2
from psycopg2.extras import execute_batch
from config import MYSQL_CONFIG, POSTGRES_CONFIG, TYPE_MAPPING

TABLE_NAME = "employees"

def migrate():
    mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
    mysql_cur = mysql_conn.cursor(dictionary=True) #Uses dictionary=True so rows are returned as:{"id": 1, "name": "Alice"}

    pg_conn = psycopg2.connect(**POSTGRES_CONFIG)
    pg_cur = pg_conn.cursor()

    try:
        # 1. Read MySQL schema
        mysql_cur.execute(f"DESCRIBE {TABLE_NAME}")
        schema = mysql_cur.fetchall()

        if not schema:
            raise RuntimeError("Table schema not found")

        # --- Identify BOOLEAN columns (TINYINT in MySQL) ---
        boolean_columns = set()
        for col in schema:
            mysql_type = col["Type"].split("(")[0].lower()
            if mysql_type == "tinyint":
                boolean_columns.add(col["Field"])

        # 2. Create PostgreSQL table
        pg_columns = []

        for col in schema:
            name = col["Field"]
            mysql_type = col["Type"].split("(")[0].lower()
            pg_type = TYPE_MAPPING.get(mysql_type, "TEXT")

            nullable = "" if col["Null"] == "YES" else "NOT NULL"

            if col["Key"] == "PRI":
                pg_columns.append(f"{name} {pg_type} PRIMARY KEY")
            else:
                pg_columns.append(f"{name} {pg_type} {nullable}")

        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            {", ".join(pg_columns)}
        );
        """

        pg_cur.execute(create_sql)
        pg_conn.commit()

        # 3. Fetch MySQL data
        mysql_cur.execute(f"SELECT * FROM {TABLE_NAME}")
        rows = mysql_cur.fetchall()

        if not rows:
            print("No rows to migrate.")
            return

        # 4. Insert data safely (with BOOLEAN conversion)
        columns = list(rows[0].keys())
        placeholders = ", ".join(["%s"] * len(columns))
        col_names = ", ".join(columns)

        insert_sql = f"""
        INSERT INTO {TABLE_NAME} ({col_names})
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
        """

        data = []
        for row in rows:
            converted_row = []
            for col in columns:
                val = row[col]
                if col in boolean_columns and val is not None:
                    converted_row.append(bool(val))
                else:
                    converted_row.append(val)
            data.append(tuple(converted_row))

        execute_batch(pg_cur, insert_sql, data, page_size=1000)
        pg_conn.commit()

        print(f"Migration completed: {len(data)} rows")

    except Exception:
        pg_conn.rollback()
        raise

    finally:
        mysql_cur.close()
        mysql_conn.close()
        pg_cur.close()
        pg_conn.close()


if __name__ == "__main__":
    migrate()
