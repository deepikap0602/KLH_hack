import streamlit as st
from backend.db import get_connection, insert_lesson, fetch_lessons
from dotenv import load_dotenv
import os
from google.genai import Client

# Load Google API key and MySQL credentials from .env
load_dotenv(dotenv_path='../frontend/.env')  # since your .env is in frontend
api_key = os.getenv("GOOGLE_API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connect to database
conn = get_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

# Create Google GenAI client
client = Client(api_key=api_key)

st.title("Lesson Planner AI")

# Form for lesson details
with st.form("lesson_form"):
    subject = st.text_input("Subject")
    topic = st.text_input("Topic")
    grade = st.text_input("Grade")
    duration = st.text_input("Duration")
    lesson_text = st.text_area("Lesson Text", height=200)

    generate_btn = st.form_submit_button("Generate Lesson")
    add_btn = st.form_submit_button("Add Lesson")

    # Generate lesson content using AI
    if generate_btn:
        if not subject.strip() or not topic.strip() or not grade.strip() or not duration.strip():
            st.warning("Please fill in Subject, Topic, Grade, and Duration before generating the lesson.")
        else:
            prompt_text = f"""
Generate a structured 7-slide classroom PowerPoint lesson plan.

Subject: {subject}
Topic: {topic}
Grade: {grade}
Duration: {duration}

Slide Structure:
Slide 1: Title Slide
Slide 2: Learning Objectives (3-5 objectives)
Slide 3: Introduction / Engagement
Slide 4: Concept Explanation
Slide 5: Classroom Activity
Slide 6: Quiz (5 MCQs + 2 Short Answer Questions)
Slide 7: Summary and Homework

Format clearly like:
Slide 1:
Content...

Slide 2:
Content...
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

    # Add lesson to database
    if add_btn:
        if not subject.strip() or not topic.strip() or not grade.strip() or not duration.strip() or not lesson_text.strip():
            st.warning("Please fill in all fields including Lesson Text before adding the lesson.")
        else:
            insert_lesson(conn, subject, topic, grade, duration, lesson_text)
            st.success("Lesson added successfully!")

# Display all lessons
st.header("All Lessons")
lessons = fetch_lessons(conn)
for lesson in lessons:
    st.subheader(f"{lesson['subject']} - {lesson['topic']} ({lesson['grade']})")
    st.write(f"Duration: {lesson['duration']}")
    st.write(lesson['lesson_text'])
    st.write(f"Created at: {lesson['created_at']}")