# database.py
import streamlit as st
from firebase_client import firebase_login, firebase_signup, get_firestore

db = get_firestore()

# ---------------- AUTH (Firebase) ----------------

def username_exists(username: str) -> bool:
    users = db.collection("users").where("username", "==", username).get()
    return len(users) > 0

def register_user(email: str, username: str, password: str):
    """Creates Firebase auth user + stores user profile in Firestore."""
    try:
        # 1. Create Firebase Auth user
        data = firebase_signup(email, password)
        user_id = data["localId"]

        # 2. Store profile in Firestore
        db.collection("users").document(user_id).set({
            "email": email,
            "username": username,
        })

        return {
            "localId": user_id,
            "email": email,
            "username": username
        }

    except Exception as e:
        st.error(f"Signup failed: {e}")
        return None


# ---------------- INTERVIEW RESULTS ----------------

def save_interview_result(result: dict):
    """
    Save interview results to Firestore.
    """
    try:
        db.collection("interview_results").add(result)
    except Exception as e:
        st.error(f"Error saving interview result: {e}")
