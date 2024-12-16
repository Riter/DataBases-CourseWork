import psycopg2
from settings import DB_CONFIG

conn = psycopg2.connect(
    **DB_CONFIG
)

with open("migrations/ddl.sql", "r", encoding="utf-8") as ddl_file, open("migrations/dml.sql", "r",encoding="utf-8") as dml_file:
    ddl_sql = ddl_file.read()
    dml_sql = dml_file.read()

try:
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(ddl_sql)
            cursor.execute(dml_sql)
    print("Инициализация завершена успешно!")
except Exception as e:
    print(f"Ошибка инициализации: {e}")
finally:
    conn.close()
