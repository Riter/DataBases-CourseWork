import streamlit as st
from services.tickets import TicketsService

def add_ticket_page():
    st.title("Добавить информацию о купленном билете")

    # Поля для ввода данных
    route_id = st.number_input("Идентификатор маршрута", min_value=1, step=1)
    price = st.number_input("Цена билета", min_value=0.0, step=0.01)
    purchase_date = st.date_input("Дата покупки")
    passenger_name = st.text_input("Имя пассажира")

    if st.button("Добавить билет"):
        if not passenger_name.strip():
            st.error("Имя пассажира не может быть пустым.")
        else:
            try:
                # Добавление билета через TicketsService
                tickets_service = TicketsService()
                tickets_service.add_ticket(route_id, price, str(purchase_date), passenger_name)
                st.success("Билет успешно добавлен!")
            except Exception as e:
                st.error(f"Ошибка при добавлении билета: {e}")
