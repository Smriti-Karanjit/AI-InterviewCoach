import streamlit as st
import json
from Theme import apply_theme, add_sidebar_navigation, require_login
from question_loader import load_questions_for_role

# ---------------- APPLY THEME FIRST ----------------
apply_theme()

# ---------------- SESSION INIT ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- REQUIRE LOGIN ----------------
require_login()

# ---------------- LOAD SIDEBAR ----------------
add_sidebar_navigation()

# ---------------- VALIDATION ----------------
required_keys = ["role", "experience", "difficulty", "question_mode"]

for key in required_keys:
    if key not in st.session_state or st.session_state[key] is None:
        st.error("Please complete previous steps first.")
        st.stop()

role = st.session_state.role
experience = st.session_state.experience
difficulty = st.session_state.difficulty
qmode = st.session_state.question_mode

# ---------------- LOAD QUESTIONS ----------------
question_bank = load_questions_for_role(role)

# ---------------- FILTER QUESTIONS ----------------
filtered = [
    q for q in question_bank
    if q["experience"].lower() == experience.lower()
    and q.get("difficulty", "").lower() == difficulty.lower()
    and q.get("category", "").lower() == qmode.lower()
]

if not filtered:
    st.warning("⚠ No questions found for this selection.")
    st.stop()

questions = [q["question"] for q in filtered]

# Save filtered list for next page
st.session_state.filtered_questions = filtered

# ---------------- PAGE HEADER ----------------
st.markdown("## Select a Question to Practice")

# ---------------- QUESTION LIST ----------------
for i, q in enumerate(questions):

    text = q if len(q) <= 150 else q[:150] + "..."

    if st.button(f"Q{i+1}: {text}", key=f"qbtn_{i}", use_container_width=True):
        st.session_state.selected_question_index = i  
        st.switch_page("pages/Practice_one.py")
