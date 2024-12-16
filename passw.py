import bcrypt
import psycopg2
from settings import DB_CONFIG

conn = psycopg2.connect(
    **DB_CONFIG
)

def get_hashed_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

hashed_password = get_hashed_password("4321")

query1 = """
        UPDATE users
        SET password = %(hashed_password)s
    """
try:
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query1, {"hashed_password": hashed_password})
finally:
    conn.close()
