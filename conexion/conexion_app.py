import os

from psycopg.rows import dict_row

from conexion.conexion import get_connection as get_mysql_connection
from conexion.conexion_postgresql import get_postgresql_connection


def usar_postgresql():
    return os.environ.get("DB_ENGINE", "mysql").lower() == "postgresql"


def get_app_connection():
    if usar_postgresql():
        return get_postgresql_connection()

    return get_mysql_connection()


def get_dict_cursor(conn):
    if usar_postgresql():
        return conn.cursor(row_factory=dict_row)

    return conn.cursor(dictionary=True)