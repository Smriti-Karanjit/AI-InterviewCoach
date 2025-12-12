import streamlit as st

# ---------------- GLOBAL SESSION INIT (MUST BE FIRST) ----------------
if "user" not in st.session_state:
    st.session_state.user = None

from Theme import apply_theme, add_sidebar_navigation, sanitize_user
from database import authenticate_user

# ---------------- APPLY THEME ----------------
apply_theme()

# ---------------- LOGIN PAGE ----------------
if st.session_state.user is None:

    # Hide sidebar on login
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    st.image("assets/logo1.png", use_container_width=True)
    st.markdown("<h2 style='text-align:center;'>Login to your account</h2>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            user = authenticate_user(username, password)

            if user:
                st.session_state.user = sanitize_user(user)
                st.switch_page("pages/Practice.py")  # redirect after login
            else:
                st.error("Incorrect username or password.")

    with col2:
        if st.button("Create an account"):
            st.switch_page("pages/Signup.py")

    st.stop()

# ---------------- AUTHENTICATED AREA ----------------

# DO NOT enforce login on every page → we remove require_login

add_sidebar_navigation()

st.markdown("""
## 🎤 Welcome to the AI Interview Coach Dashboard  
Start practicing interview questions and receive instant AI feedback.
""")
