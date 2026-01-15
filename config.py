MYSQL_CONFIG = {
    "host": "localhost",   # now OK
    "port": 3306,
    "user": "root",
    "password": "rootpassword",
    "database": "demo_mysql",
    "auth_plugin": "caching_sha2_password",
    "use_pure": True,
    "ssl_disabled": True
}
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "shtlpmac027",
    "dbname": "demo_postgres",
}

TYPE_MAPPING = {
    "int": "INTEGER",
    "bigint": "BIGINT",
    "varchar": "VARCHAR",
    "text": "TEXT",
    "datetime": "TIMESTAMP",
    "timestamp": "TIMESTAMP",
    "date": "DATE",
    "float": "REAL",
    "double": "DOUBLE PRECISION",
    "decimal": "NUMERIC",
    "json": "JSONB",
    "tinyint": "BOOLEAN",   # common MySQL pattern
}
