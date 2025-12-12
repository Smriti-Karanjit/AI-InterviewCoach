import streamlit as st
from Theme import apply_theme
from database import register_user, username_exists

apply_theme()

# Hide sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;margin-top:20px;'>Create Your Account</h2>", unsafe_allow_html=True)

email = st.text_input("Email")
password = st.text_input("Password", type="password")

# FIX WHITE BUTTON (THEME OVERRIDE)
st.markdown("""
<style>
.stButton > button {
    background-color: #0078ff !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px !important;
    font-weight: 600 !important;
    border: none !important;
}
.stButton > button:hover {
    background-color: #005fcc !important;
}
</style>
""", unsafe_allow_html=True)

if st.button("Sign Up", use_container_width=True):

    if username_exists(email):
        st.warning("This email is already registered. Please log in instead.")
        st.stop()

    user = register_user(email, password)  # <-- ONLY THESE 2 ARGUMENTS

    if user:
        st.success("🎉 Account created successfully! Please log in.")
        st.switch_page("pages/Login.py")
