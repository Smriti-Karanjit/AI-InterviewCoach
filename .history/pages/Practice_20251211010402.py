import streamlit as st
from Theme import apply_theme, add_sidebar_navigation, require_login

# Session init
if "user" not in st.session_state:
    st.session_state.user = None

apply_theme()
require_login()
add_sidebar_navigation()

st.markdown("<h2 style='text-align:center;'>Practice Mode</h2>", unsafe_allow_html=True)

roles = [
    "QA Analyst",
    "Data Scientist",
    "Marketing Associate",
    "DevOps Engineer",
    "HR Specialist",
    "Software Engineer",
    "Product Manager",
    "UX Designer",
    "Coming Soon"
]

cols = st.columns(3)

for i, role in enumerate(roles):
    with cols[i % 3]:

        # Render a simple button
        if st.button(role, key=f"role_{i}"):
            st.session_state.role = role
            st.switch_page("pages/Practice_experience.py")
