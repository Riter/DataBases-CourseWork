import psycopg2
import streamlit as st
from settings import DB_CONFIG

def call_assign_drivers():
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL assign_drivers();")
                conn.commit()
        st.success("Автоматическое назначение водителей выполнено.")
    except Exception as e:
        st.error(f"Ошибка при назначении водителей: {e}")
