import pandas as pd
import streamlit as st
from services.routes import RoutesService

def show_routes_page():
    """
        Показ расписания маршрутов вместе с информацией о водителях, 
        включая маршруты без назначенных водителей
    """

    st.title("Расписание маршрутов")
    
    routes_service = RoutesService()
    
    # Получение полного расписания
    schedule = routes_service.get_schedule()
    
    # Уникальные имена водителей
    drivers = ["Все водители"] + schedule["driver_name"].unique().tolist()
    
    # Выбор водителя
    selected_driver = st.selectbox("Выберите водителя", drivers)
    
    # Фильтрация расписания по выбранному водителю
    if selected_driver != "Все водители":
        schedule = schedule[schedule["driver_name"] == selected_driver]
    
    # Отображение таблицы
    st.dataframe(schedule)
