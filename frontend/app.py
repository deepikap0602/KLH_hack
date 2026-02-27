import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
from google.genai import Client

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize GenAI client
client = Client(api_key=api_key)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # Change if needed
        user="root",       # Your MySQL username
        password="",       # Your MySQL password
        database="lesson_planner"
    )

# Function to generate lesson plan
def generate_lesson(subject, topic, grade, duration):
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

And so on.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_text
    )
    return response.text

# Streamlit UI
st.title("Teacher's Lesson Plan Architect")

with st.form(key="lesson_form"):
    subject = st.text_input("Subject", "Maths")
    topic = st.text_input("Topic", "Algebraic Expressions")
    grade = st.text_input("Grade", "10")
    duration = st.text_input("Duration", "40 minutes")
    submit = st.form_submit_button("Generate Lesson Plan")

if submit:
    with st.spinner("Generating lesson plan..."):
        lesson_plan_text = generate_lesson(subject, topic, grade, duration)
        st.subheader("Generated Lesson Plan")
        st.text_area("Lesson Plan", lesson_plan_text, height=500)

        # Save to database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO lesson_plans (subject, topic, grade, duration, lesson_text) VALUES (%s, %s, %s, %s, %s)",
                (subject, topic, grade, duration, lesson_plan_text)
            )
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Lesson plan saved to database!")
        except Exception as e:
            st.error(f"Failed to save to database: {e}")