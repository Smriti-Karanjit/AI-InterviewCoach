import streamlit as st
from firebase_client import firebase_login, firebase_signup, get_firestore

db = get_firestore()


# --------------------------
# CHECK IF USERNAME EXISTS
# --------------------------
def username_exists(username: str):
    """Check if username already exists in Firestore."""
    try:
        users = db.collection("users").where("username", "==", username).stream()
        return any(users)
    except Exception as e:
        st.error(f"Error checking username: {e}")
        return False


# --------------------------
# REGISTER USER (3 ARGUMENTS)
# --------------------------
def register_user(email: str, username: str, password: str):
    """Create Firebase Auth user + store username/email in Firestore."""
    try:
        auth_data = firebase_signup(email, password)

        user_record = {
            "username": username,
            "email": email,
            "localId": auth_data["localId"]
        }

        # Save in Firestore
        db.collection("users").document(auth_data["localId"]).set(user_record)

        return user_record

    except Exception as e:
        st.error(f"Signup failed: {e}")
        return None


# --------------------------
# LOGIN USER (2 ARGUMENTS)
# --------------------------
def authenticate_user(email: str, password: str):
    try:
        data = firebase_login(email, password)
        return {
            "email": email,
            "localId": data["localId"],
            "idToken": data["idToken"]
        }
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None


# --------------------------
# SAVE INTERVIEW RESULT
# --------------------------
def save_interview_result(result: dict):
    try:
        db.collection("interview_results").add(result)
    except Exception as e:
        st.error(f"Error saving result: {e}")
