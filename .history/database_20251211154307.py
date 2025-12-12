# database.py
import streamlit as st
from firebase_client import firebase_login, firebase_signup, get_firestore

db = get_firestore()

# ---------------- AUTH ----------------

def authenticate_user(email: str, password: str):
    """
    Use Firebase Auth login.
    Returns a user dict if success, else None.
    """
    try:
        data = firebase_login(email, password)
        # You can store more, but at minimum:
        return {
            "email": email,
            "localId": data.get("localId"),
            "idToken": data.get("idToken")
        }
    except ValueError as e:
        st.error(f"Login failed: {e}")
        return None


def register_user(email: str, password: str):
    """
    Create a new user in Firebase Auth.
    """
    try:
        data = firebase_signup(email, password)
        return {
            "email": email,
            "localId": data.get("localId"),
            "idToken": data.get("idToken")
        }
    except ValueError as e:
        st.error(f"Signup failed: {e}")
        return None


# ---------------- INTERVIEW RESULTS ----------------

def save_interview_result(result: dict):
    """
    Save an interview result document into Firestore.
    `result` is expected to be a dict (you already build this in Practice page).
    """
    try:
        db.collection("interview_results").add(result)
    except Exception as e:
        st.error(f"Error saving result: {e}")
