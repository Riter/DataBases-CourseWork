import psycopg2
import psycopg2.extras
from settings import DB_CONFIG
from pandas import DataFrame

def get_users() -> list[dict]:
    print("Receiving users")
    query = "SELECT user_id, nickname, email FROM users;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

def get_users_with_password() -> list[dict]:
    print("Receiving users")
    query = "SELECT password, email FROM users;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

def get_user_by_email(user_email) -> list[dict]:
    query = "SELECT user_id, nickname, email FROM users WHERE email = %(email)s"

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"email" : user_email})
            return cur.fetchall()