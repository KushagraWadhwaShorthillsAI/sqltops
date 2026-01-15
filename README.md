# MySQL to PostgreSQL Migration

This project contains scripts to load dummy employee data into MySQL and migrate it to PostgreSQL.

## Files

- `dummy_dataset.sql` - SQL file with CREATE TABLE and INSERT statements (100 rows, 15 columns)
- `load_to_mysql.sh` - Bash script to load data into MySQL
- `migrate_to_postgres.py` - Python script to migrate data from MySQL to PostgreSQL
- `requirements.txt` - Python dependencies

## Prerequisites

1. **MySQL** installed and running
2. **PostgreSQL** installed and running
3. **Python 3.6+** installed
4. **pip** for installing Python packages

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Databases

**MySQL:**
```sql
CREATE DATABASE testdb;
```

**PostgreSQL:**
```sql
CREATE DATABASE testdb;
```

## Usage

### Step 1: Load Data into MySQL

**Option A: Using the Python script (Recommended - works even if mysql CLI not in PATH)**
```bash
# Run with default settings
python load_to_mysql.py

# Or specify custom parameters
python load_to_mysql.py --database testdb --user root --password yourpass
python load_to_mysql.py -d mydb -u myuser -p mypass --host localhost --port 3306
```

**Option B: Using the shell script**
```bash
# Make script executable
chmod +x load_to_mysql.sh

# Run with default settings (database: testdb, user: root, no password)
./load_to_mysql.sh

# Or specify custom parameters
./load_to_mysql.sh [database_name] [username] [password] [host] [port]
./load_to_mysql.sh mydb myuser mypass localhost 3306
```

**Option C: Using MySQL command directly**
```bash
mysql -u root -p testdb < dummy_dataset.sql
```

**Note:** If you get "mysql: command not found", use Option A (Python script) instead.

### Step 2: Configure Connection Parameters

Edit `migrate_to_postgres.py` and update the connection parameters:

```python
# MySQL connection parameters
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_mysql_password',
    'database': 'testdb'
}

# PostgreSQL connection parameters
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'your_postgres_password',
    'database': 'testdb'
}
```

**Alternative: Use Environment Variables**

You can also set environment variables instead of editing the file:

```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=testdb

export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=your_password
export POSTGRES_DATABASE=testdb
```

### Step 3: Run Migration Script

```bash
python migrate_to_postgres.py
```

Or make it executable and run directly:
```bash
chmod +x migrate_to_postgres.py
./migrate_to_postgres.py
```

## What the Migration Script Does

1. **Connects** to both MySQL and PostgreSQL databases
2. **Reads** the table schema from MySQL
3. **Creates** the equivalent table in PostgreSQL (with proper type mapping)
4. **Fetches** all data from MySQL
5. **Inserts** all data into PostgreSQL

## Data Type Mappings

The script automatically maps MySQL types to PostgreSQL types:

| MySQL Type | PostgreSQL Type |
|------------|----------------|
| INT | INTEGER |
| VARCHAR(n) | VARCHAR(n) |
| DECIMAL(p,s) | DECIMAL(p,s) |
| DATE | DATE |
| TINYINT(1) / BOOLEAN | BOOLEAN |
| TEXT | TEXT |

## Verification

After migration, verify the data in PostgreSQL:

```sql
-- Connect to PostgreSQL
psql -U postgres -d testdb

-- Check row count
SELECT COUNT(*) FROM employees;

-- View sample data
SELECT * FROM employees LIMIT 10;
```

## Troubleshooting

### MySQL Connection Issues
- Ensure MySQL is running: `mysqladmin -u root -p status`
- Check if database exists: `mysql -u root -p -e "SHOW DATABASES;"`
- Verify user permissions

### PostgreSQL Connection Issues
- Ensure PostgreSQL is running: `pg_isready`
- Check if database exists: `psql -U postgres -l`
- Verify user permissions and password

### Python Package Issues
- Make sure you're using Python 3: `python3 --version`
- Try installing packages with `pip3` instead of `pip`
- On macOS, you might need: `pip3 install --user -r requirements.txt`

### Permission Issues
- Make scripts executable: `chmod +x load_to_mysql.sh migrate_to_postgres.py`
- Ensure database users have CREATE and INSERT permissions

## Notes

- The script will **drop and recreate** the table in PostgreSQL if it already exists
- All data types are automatically converted to PostgreSQL equivalents
- The migration preserves all data including NULL values
- Primary keys and constraints are maintained
