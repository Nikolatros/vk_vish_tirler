from dataclasses import dataclass
import pandas as pd
import psycopg2
from psycopg2.extensions import connection, cursor
from config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD


@dataclass
class DBWriter:
    conn: connection = None
    cur: cursor = None
    __POSTGRES_DB: str = POSTGRES_DB
    __POSTGRES_USER: str = POSTGRES_USER
    __POSTGRES_PASSWORD: str | int = POSTGRES_PASSWORD

    def db_connect(self) -> None:
        """Connects to database"""
        self.conn = psycopg2.connect(
            dbname=self.__POSTGRES_DB,
            user=self.__POSTGRES_USER,
            password=self.__POSTGRES_PASSWORD,
            host="db",
        )
        self.cur = self.conn.cursor()

    def insert_data(self, posts: pd.DataFrame) -> None:
        """Insert data to database

        Args:
            posts (pd.DataFrame): data to insert
        """
        # Check connection to database
        assert all(
            (self.conn, self.cur)
        ), "Database is not connected. Call db.connection()"

        columns = posts.columns

        # Genearte insert query for postgresql table
        insert_query = f"INSERT INTO vish_posts ({", ".join(posts.columns)}) \
            VALUES (f{'%s' * len(columns)})"

        # Insert data to table
        self.cur.executemany(
            query=insert_query,
            insert_query=[posts[column] for column in columns],
        )
        self.conn.commit()

    def db_disconnect(self) -> None:
        """Disconnects from database"""
        self.cur.close()
        self.conn.close()
