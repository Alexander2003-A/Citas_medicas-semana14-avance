import os
import psycopg


def get_postgresql_connection():
    return psycopg.connect(
        host=os.environ["PG_HOST"],
        port=os.environ.get("PG_PORT", "5432"),
        user=os.environ["PG_USER"],
        password=os.environ["PG_PASSWORD"],
        dbname=os.environ["PG_DATABASE"]
    )