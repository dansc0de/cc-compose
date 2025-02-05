################################################
# This file is used to define the database connections
# for the application. Do not alter this file.
################################################
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgrespassword@postgres:5432/tasksdb"
)


def init_db():
    """
    Initialize the PostgreSQL database by creating the tasks table if it does not exist.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def get_db_connection():
    """
    Get a new database connection that returns rows as dictionaries.
    """
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    conn.autocommit = True
    return conn
