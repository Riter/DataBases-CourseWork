import streamlit as st
import repositories.users
from services.auth import Authotize
import services.user
import services.users
import services.regist
import services.session
import repositories.admin
import pandas as pd
from pages.route import show_routes_page
from pages.tickets import show_tickets_page
from pages.add_ticket import add_ticket_page
from pages.assign_driver import assign_drivers_page

import psycopg2
from settings import DB_CONFIG

auth = Authotize()
users = services.users.get_users()
registr = services.regist.Registration()

def login():
    st.title("Авторизация")
    st.write("Введите почту и пароль:")

    email = st.text_input("Почта")
    password = st.text_input("Пароль", type="password")
    if st.button("Войти"):
        if auth.auth(email, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = email
            st.success(f"Добро пожаловать, {email}!")
            st.session_state.user = services.user.get_user(email)
            st.session_state["admin"] = repositories.admin.get_admins(st.session_state.user["user_id"].item())
            print(st.session_state["admin"])
            st.rerun()
        else:
            st.error("Неверная почта или пароль!")

def register():
    st.title("Регистрация")
    st.write("Введите почту")
    email = st.text_input("Почта")
    st.write("Введите пароль")
    password = st.text_input("Пароль", type="password")
    st.write("Подтвердите пароль")
    second_password = st.text_input("Подтверждение пароля", type="password")
    st.write("Введите ник")
    nickname = st.text_input("Ник")

    if st.button("Зарегистрироваться"):
        if (not(email) or not(password) or not(second_password) or not(nickname)):
            st.error("Введите требуемые значения!")
        else:
            if (password != second_password):
                st.error("Пароли не совпадают!")
            else:
                if users["email"].isin([email]).any():
                    st.error("Данная почта уже зарегистрирована!")
                elif users["nickname"].isin([nickname]).any():
                    st.error("Пользователь с данным именем уже существует")
                else:
                    st.success("Успешная регистрация")
                    st.session_state["authenticated"] = True
                    user_id = registr.registr(pd.DataFrame({"nickname": [nickname], "email": [email], "password": [password]}))
                    user = pd.DataFrame({"user_id": [user_id], "nickname": [nickname], "email": [email], "password": [password]})
                    st.session_state.user = user
                    st.rerun()


def main():

    if not st.session_state["authenticated"]:
        pg = st.radio("Войдите или зарегистрируйтесь", ["Вход", "Регистрация"])
        if pg == "Вход":
            login()
        elif pg == "Регистрация":
            register()
    else:

        if st.session_state["admin"]:
            page = st.sidebar.radio(
                "Перейти к странице",
                ["Маршруты", "Купленные билеты", "Добавить покупку", "Назначить водителя"],
            )

            if page == "Маршруты":
                show_routes_page()
            elif page == "Купленные билеты":
                show_tickets_page()
            elif page == "Добавить покупку":
                add_ticket_page()
            elif page == "Назначить водителя":
                assign_drivers_page()

        else:
            page = st.sidebar.radio(
                "Перейти к странице",
                ["Маршруты", "Купленные билеты", "Назначить водителя"],
            )

            if page == "Маршруты":
                show_routes_page()
            elif page == "Купленные билеты":
                show_tickets_page()
            elif page == "Назначить водителя":
                assign_drivers_page()

services.session.init_session()

if __name__ == "__main__":
    main()
