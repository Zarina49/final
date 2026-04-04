# ==============================
# Daily Reflection & Self-Assessment Survey
# ==============================

import streamlit as st
import json
from datetime import datetime

version_float = 1.1

# ---------------- QUESTIONS ----------------
questions = [
    {"q": "How often do you write down what you learned each day?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you reflect on your mistakes after studying?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you think about how to improve your next study session?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you evaluate your academic performance?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you set learning goals for yourself?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you check if you achieved your study goals?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you plan your study time in advance?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you follow your study schedule?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you avoid procrastination?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you feel motivated to improve your learning?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you understand your strengths and weaknesses?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you adjust your study methods when needed?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]}
]

# ---------------- REFLECTION LEVELS ----------------
reflection_levels = {
    "Excellent Reflection Habits": (0, 15),
    "Good Reflection Practice": (16, 30),
    "Moderate Reflection": (31, 45),
    "Weak Reflection Habits": (46, 60),
    "Poor Reflection Habits": (61, 100)
}

# ---------------- FUNCTIONS ----------------
def validate_name(name):
    return name.strip() != "" and not any(char.isdigit() for char in name)

def validate_dob(dob):
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score):
    for level, (low, high) in reflection_levels.items():
        if low <= score <= high:
            return level
    return "Unknown"

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- UI ----------------
st.set_page_config(page_title="Reflection Survey")
st.title("📘 Daily Reflection & Self-Assessment Survey")

st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# --- Start Survey ---
if st.button("Start Survey"):

    errors = []

    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date format (use YYYY-MM-DD).")
    if not sid.isdigit():
        errors.append("Student ID must contain only digits.")

    if errors:
        for error in errors:
            st.error(error)

    else:
        st.success("All inputs are valid. Please answer the questions below.")

        total_score = 0
        answers = []

        for i, q in enumerate(questions):
            labels = [opt[0] for opt in q["opts"]]

            choice = st.selectbox(
                f"Q{i+1}. {q['q']}",
                labels,
                key=f"q{i}"
            )

            score = next(val for label, val in q["opts"] if label == choice)

            total_score += score

            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        # --- Result ---
        result = interpret_score(total_score)

        st.markdown("## 📊 Your Reflection Level")
        st.write(f"**Total Score:** {total_score}")
        st.write(f"**Result:** {result}")

        # --- Save ---
        data = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": result,
            "answers": answers,
            "version": version_float
        }

        filename = f"{sid}_reflection_result.json"
        save_json(filename, data)

        st.success(f"Results saved as {filename}")

        st.download_button(
            "Download your result",
            json.dumps(data, indent=2),
            file_name=filename
        )