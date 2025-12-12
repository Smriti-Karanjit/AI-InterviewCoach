import streamlit as st

# ---------- SESSION INIT ----------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------- IMPORT THEME ----------
from Theme import apply_theme, add_sidebar_navigation

# ---------- THEME & SIDEBAR ----------
apply_theme()
add_sidebar_navigation()

# ---------- VALIDATION ----------
if "role" not in st.session_state or st.session_state.role is None:
    st.error("Please select a role first.")
    st.stop()

role = st.session_state.role

# ---------- HEADER ----------
st.markdown(
    f"<h2 style='text-align:center;margin-top:10px;'>Role: {role}</h2>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='margin-top:12px;'>Select your experience level</h3>",
    unsafe_allow_html=True
)

# ---------- EXPERIENCE OPTIONS ----------
experience_levels = [
    "Fresher", "Intern", "1 year", "2 years", "3 years", "4 years",
    "5 years", "6 years", "7+ years"
]

# ---------- GRID ----------
cols = st.columns(3)

for i, level in enumerate(experience_levels):
    with cols[i % 3]:
        if st.button(level, key=f"exp_{level}", use_container_width=True):
            st.session_state.experience = level
            st.switch_page("pages/Practice_Difficulty.py")

# ---------- CSS (FIXED — NO EXTRA BLOCKS) ----------
st.markdown("""
<style>

div.stButton > button {
    padding: 18px !important;
    background: rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0,191,255,0.25) !important;
    margin-top: 10px !important;
    margin-bottom: 14px !important;
    text-align: center !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    transition: 0.2s ease-in-out;
}

div.stButton > button:hover {
    background: rgba(0,191,255,0.25) !important;
    border: 1px solid rgba(0,191,255,0.7) !important;
}

</style>
""", unsafe_allow_html=True)
