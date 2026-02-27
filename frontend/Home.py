import streamlit as st
import sys
import os
from dotenv import load_dotenv

# 🔥 Fix backend import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.db import get_connection, create_user, check_user

# Load .env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

conn = get_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

# -------- SESSION STATE --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -------- TITLE --------
st.title("Login / Sign Up")

choice = st.radio("Select Action:", ["Login", "Sign Up"])

# ================= SIGN UP =================
if choice == "Sign Up":
    username = st.text_input("Username", key="signup_user")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pw")

    if st.button("Sign Up"):
        if username and email and password:
            create_user(conn, username, email, password)
            st.success("Account created! Please login.")
        else:
            st.warning("Fill all fields.")

# ================= LOGIN =================
else:
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pw")

    if st.button("Login"):
        user = check_user(conn, username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.username = username

            # ✅ Correct way for multipage
            st.switch_page("pages/LessonApp.py")

        else:
            st.error("Incorrect username or password.")