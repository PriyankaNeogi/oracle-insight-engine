import duckdb
from backend.config import settings

conn = duckdb.connect(settings.SQL_DB_PATH)


def run_sql(query: str):
    try:
        return conn.execute(query).fetchall()
    except Exception as e:
        return str(e)