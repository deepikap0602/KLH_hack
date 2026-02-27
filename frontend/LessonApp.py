import streamlit as st
import os
from dotenv import load_dotenv
from backend.db import get_connection, insert_lesson, fetch_lessons
from google.genai import Client

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Check login ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()

st.title(f"Lesson Planner AI - Welcome {st.session_state['username']}")

client = Client(api_key=API_KEY)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
conn = get_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

# --- Lesson Planner UI (same as app.py) ---
with st.form("lesson_form"):
    subject = st.text_input("Subject")
    topic = st.text_input("Topic")
    grade = st.text_input("Grade")
    duration = st.text_input("Duration")
    lesson_text = st.text_area("Lesson Text", height=200)

    generate_btn = st.form_submit_button("Generate Lesson")
    add_btn = st.form_submit_button("Add Lesson")

    if generate_btn:
        if not subject.strip() or not topic.strip() or not grade.strip() or not duration.strip():
            st.warning("Please fill in all fields before generating the lesson.")
        else:
            prompt_text = f"""
Generate a structured 7-slide classroom PowerPoint lesson plan.
Subject: {subject}
Topic: {topic}
Grade: {grade}
Duration: {duration}
"""
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_text
                )
                lesson_text = response.text
                st.text_area("Lesson Text", value=lesson_text, height=300)
                st.success("Lesson generated successfully!")
            except Exception as e:
                st.error(f"Error generating lesson: {e}")

    if add_btn:
        if not subject.strip() or not topic.strip() or not grade.strip() or not duration.strip() or not lesson_text.strip():
            st.warning("Please fill in all fields including Lesson Text before adding the lesson.")
        else:
            insert_lesson(conn, subject, topic, grade, duration, lesson_text)
            st.success("Lesson added successfully!")

st.header("All Lessons")
lessons = fetch_lessons(conn)
for lesson in lessons:
    st.subheader(f"{lesson['subject']} - {lesson['topic']} ({lesson['grade']})")
    st.write(f"Duration: {lesson['duration']}")
    st.write(lesson['lesson_text'])
    st.write(f"Created at: {lesson['created_at']}")