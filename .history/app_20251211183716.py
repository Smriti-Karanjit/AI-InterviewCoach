import streamlit as st

# ---------------- GLOBAL SESSION INIT (MUST BE FIRST) ----------------
if "user" not in st.session_state:
    st.session_state.user = None

from Theme import apply_theme, add_sidebar_navigation, sanitize_user
from database import authenticate_user  # now Firebase-based


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

    st.markdown("<h3 style='text-align:center;'>Login to your account</h3>", unsafe_allow_html=True)

    # ---------------- USER INPUT ----------------
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # ---------------- BUTTONS ----------------
    login_col, signup_col = st.columns(2)

    with login_col:
        if st.button("Login", use_container_width=True):
            user = authenticate_user(email, password)

            if user:
                st.session_state.user = sanitize_user(user)
                st.success("Login successful! Redirecting…")
                st.switch_page("pages/Practice.py")
            else:
                st.error("Invalid email or password")

    with signup_col:
        if st.button("Create an account", use_container_width=True):
            st.switch_page("pages/Signup.py")

    st.stop()


# ---------------- AUTHENTICATED AREA ----------------

add_sidebar_navigation()

# Sticky header at top of dashboard
st.markdown("""
<div style="position:sticky; top:0; background:#001230; padding:10px 15px;
     border-bottom:1px solid rgba(255,255,255,0.15); z-index:1000;">
     <h3 style="color:#e0f7ff; margin:0;">AI Interview Coach Dashboard</h3>
</div>
""", unsafe_allow_html=True)

# Main dashboard text
st.markdown("""
## 🎤 Welcome!
Start practicing interview questions and receive instant AI-powered feedback.
""")
