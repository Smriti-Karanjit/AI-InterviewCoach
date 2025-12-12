import streamlit as st
from Theme import apply_theme, add_sidebar_navigation, require_login
from question_loader import load_questions_for_role

apply_theme()
if "user" not in st.session_state:
    st.session_state.user = None
require_login()
add_sidebar_navigation()

# Validation
required_keys = ["role", "experience", "difficulty", "question_mode"]
for k in required_keys:
    if k not in st.session_state or st.session_state[k] is None:
        st.error("Please complete previous steps first.")
        st.stop()

role = st.session_state.role
experience = st.session_state.experience
difficulty = st.session_state.difficulty
mode = st.session_state.question_mode

# Load role-specific questions
question_bank = load_questions_for_role(role)

# Filter
filtered = [
    q for q in question_bank
    if q["experience"].lower() == experience.lower()
    and q["difficulty"].lower() == difficulty.lower()
    and q["category"].lower() == mode.lower()
]

if not filtered:
    st.warning("⚠ No questions found for this selection.")
    st.stop()

# Save for next page
st.session_state.filtered_questions = filtered

st.markdown("## Select a Question")

for i, q in enumerate(filtered):
    preview = q["question"][:150] + "..." if len(q["question"]) > 150 else q["question"]

    if st.button(f"Q{i+1}: {preview}", key=f"q{i}", use_container_width=True):
        st.session_state.selected_question_index = i
        st.switch_page("pages/Practice_one.py")
