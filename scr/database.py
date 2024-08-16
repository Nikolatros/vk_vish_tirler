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

    def is_connected(self) -> bool:
        """Check that database is connected

        Returns:
            bool: True if database is connected else False
        """
        return all((self.conn, self.cur))

    def db_connect(self) -> None:
        """Connects to database"""
        print("Connecting to database...")
        self.conn = psycopg2.connect(
            dbname=self.__POSTGRES_DB,
            user=self.__POSTGRES_USER,
            password=self.__POSTGRES_PASSWORD,
            host="db",
        )
        self.cur = self.conn.cursor()
        print("DATABASE IS CONNECTED\n")

    def insert_data(self, posts: pd.DataFrame) -> None:
        """Insert data to database

        Args:
            posts (pd.DataFrame): Data to insert
        """
        print("Inserting data to database...")

        # Check connection to database
        if not self.is_connected():
            raise ConnectionError("""Database is not connected""")

        columns = posts.columns

        # Generate insert query for postgresql table
        insert_query = f"INSERT INTO vish_posts ({', '.join(columns)}) \
                VALUES ({', '.join(['%s'] * len(columns))}) \
                ON CONFLICT (id) DO NOTHING"

        # Insert data to table
        self.cur.executemany(
            query=insert_query,
            vars_list=[tuple(row) for row in posts.to_numpy()],
        )
        self.conn.commit()
        print(f"{len(posts)} rows are inserted \n")

    def db_disconnect(self) -> None:
        """Disconnects from database"""
        self.cur.close()
        self.conn.close()
        print("DISCONNECTED FROM DATABASE\n")
