import psycopg2
from config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD


def db_connection():
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host='db'
    )
    return conn


def insert_to_table(table_name):