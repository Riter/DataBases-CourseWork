import psycopg2
from contextlib import contextmanager

import psycopg2.pool
from settings import DB_CONFIG, POOL_MIN_CONN, POOL_MAX_CONN
import atexit

print("Initializing connection pool...")
connection_pool = psycopg2.pool.SimpleConnectionPool(
    POOL_MIN_CONN, POOL_MAX_CONN, **DB_CONFIG
)

@contextmanager
async def get_connection():
    connection = connection_pool.getconn()
    try:
        yield connection
    finally:
        connection_pool.putconn(connection)

def close_connection_pool():
    if connection_pool:
        connection_pool.closeall()
        print("Connection pool closed!")

def on_exit():
    print("work is over!")
    close_connection_pool()

atexit.register(on_exit)
