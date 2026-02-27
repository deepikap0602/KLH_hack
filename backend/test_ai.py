import os
from dotenv import load_dotenv
from google.genai import Client

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Google API Key not found in .env")

# Create client with API key
client = Client(api_key=api_key)

# Your lesson prompt
subject = "Maths"
topic = "Algebraic Expressions"
grade = "10"
duration = "40 minutes"

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

try:
    # Call the API correctly using generate_content
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_text
    )

    # Print the generated result
    print("\n===== GENERATED PRESENTATION =====\n")
    print(response.text)

except Exception as e:
    print("Error:", e)