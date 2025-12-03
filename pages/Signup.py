import streamlit as st
from Theme import apply_theme
from database import create_user,get_user_by_username

apply_theme()
st.set_page_config(page_title="Sign Up | AI Interview Coach", layout="centered")

# --- APP LOGO (your real logo visible) ---
st.image("assets/logo1.png", use_container_width=True)
st.markdown("<h2 style='text-align:center;margin-top:10px;'>Create Your Account</h2>", unsafe_allow_html=True)
st.write("Join the AI Interview Coach community and level up your interview skills 🚀")

# --- SIGNUP FORM ---
with st.form(key="signup_form"):
    username = st.text_input("Username", placeholder="Create a username")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter a strong password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Retype your password")
    submitted = st.form_submit_button("Sign Up")

if submitted:
        if not username or not email or not password or not confirm_password:
            st.error("Please fill all fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif get_user_by_username(username):
            st.error("Username already taken.")
        else:
            create_user(email,username,password)
            st.success("Account created successfully!")
            st.balloons()
            st.info("You can now login.")
            if st.button("⬅ Back to Login"):
                st.switch_page("app.py")
