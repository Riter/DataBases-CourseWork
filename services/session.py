import streamlit as st
import pandas as pd

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if "admin" not in st.session_state:
        st.session_state["admin"] = False
    
    if "user" not in st.session_state:
        st.session_state.user = pd.DataFrame(
            columns = ["user_id", "nickname", "email"]
        )
