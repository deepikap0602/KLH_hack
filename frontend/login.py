import streamlit as st
from backend.db import get_connection, create_user, check_user
import os
from dotenv import load_dotenv

# Load DB credentials
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

conn = get_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
if not conn:
    st.error("Database connection failed.")
    st.stop()

st.title("Lesson Planner AI - Login / Signup")

choice = st.radio("Select Action:", ["Login", "Sign Up"])

if choice == "Sign Up":
    st.subheader("Create New Account")
    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    signup_btn = st.button("Sign Up")

    if signup_btn:
        if new_username and new_email and new_password:
            create_user(conn, new_username, new_email, new_password)
            st.success("Account created! Please login.")
        else:
            st.warning("Please fill all fields.")

else:  # Login
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username and password:
            user = check_user(conn, username, password)
            if user:
                st.success(f"Welcome {username}!")
                # Redirect to main app
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
            else:
                st.error("Incorrect username or password.")
        else:
            st.warning("Please enter both username and password.")