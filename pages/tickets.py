import streamlit as st
from services.tickets import TicketsService

def show_tickets_page():
    st.title("Купленные билеты")
    
    # Инициализация сервиса для работы с билетами
    tickets_service = TicketsService()
    
    # Получение данных о купленных билетах
    tickets = tickets_service.get_tickets()
    
    # Проверка, есть ли билеты
    if tickets.empty:
        st.write("Билеты не найдены.")
    else:
        # Фильтр по имени пассажира
        passenger_name = st.text_input("Введите имя пассажира для фильтрации (оставьте пустым для отображения всех билетов):")
        
        # Фильтрация билетов по имени пассажира
        if passenger_name:
            tickets = tickets[tickets["passenger_name"].str.contains(passenger_name, case=False, na=False)]
        
        # Проверка, есть ли результаты после фильтрации
        if tickets.empty:
            st.write("Билеты с указанным именем пассажира не найдены.")
        else:
            # Отображение таблицы с билетами
            st.dataframe(tickets)
