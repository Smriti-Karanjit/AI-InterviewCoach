import streamlit as st
from firebase_client import firebase_login, firebase_signup, get_firestore

db = get_firestore()

# ----------- CHECK IF USERNAME OR EMAIL EXISTS -----------

def username_exists(email: str):
    """Check if user email already exists in Firestore."""
    try:
        users_ref = db.collection("users")
        query = users_ref.where("email", "==", email).stream()
        return any(query)
    except Exception as e:
        st.error(f"Error checking username: {e}")
        return False

# ----------- SIGN UP -----------

def register_user(email: str, password: str):
    """Create new Firebase Auth user + save user profile in Firestore."""
    try:
        data = firebase_signup(email, password)

        user_data = {
            "email": email,
            "localId": data["localId"]
        }

        # Save user in Firestore users table
        db.collection("users").document(data["localId"]).set(user_data)

        return user_data

    except Exception as e:
        st.error(f"Signup failed: {e}")
        return None

# ----------- LOGIN -----------

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

# ----------- SAVE INTERVIEW RESULT -----------

def save_interview_result(result: dict):
    """Save interview performance into Firestore."""
    try:
        db.collection("interview_results").add(result)
    except Exception as e:
        st.error(f"Error saving result: {e}")
