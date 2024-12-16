import streamlit as st
from services.assign_driver import AssignDriverService

def assign_drivers_page():
    st.title("Автоматическое назначение водителей")
    st.write("Назначение водителей на маршруты на основе опыта и расписания.")

    if st.button("Назначить водителей"):
        assign_driver_service = AssignDriverService()
        assign_driver_service.assign_drivers()
