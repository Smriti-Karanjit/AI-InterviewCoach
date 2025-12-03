import streamlit as st
import json
from Theme import apply_theme, add_sidebar_navigation, require_login
from question_loader import QUESTIONS

# ---------------- APPLY THEME FIRST ----------------
apply_theme()

# ---------------- SESSION INIT (IMPORTANT) ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- REQUIRE LOGIN ----------------
require_login()

# ---------------- LOAD SIDEBAR ----------------
add_sidebar_navigation()

# ---------------- LOAD QUESTIONS ----------------
question_bank = QUESTIONS

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

# ---------------- FILTER QUESTIONS ----------------
filtered = [
    q for q in question_bank
    if q["role"].lower() == role.lower()
    and q["experience"].lower() == experience.lower()
    and q["difficulty"].lower() == difficulty.lower()
    and q["source_type"].lower() == qmode.lower()
]

if not filtered:
    st.warning("⚠ No questions found for this selection.")
    st.stop()

questions = [q["question"] for q in filtered]

# ---------------- PAGE HEADER ----------------
st.markdown("## Select a Question to Practice")

# ---------------- QUESTION LIST ----------------
for i, q in enumerate(questions):

    text = q if len(q) <= 150 else q[:150] + "..."

    if st.button(f"Q{i+1}: {text}", key=f"qbtn_{i}", use_container_width=True):

        # Save selected index into session
        st.session_state.selected_question_index = i  

        # Navigate to Practice One page
        st.switch_page("pages/Practice_one.py")
