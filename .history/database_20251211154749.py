# database.py
import streamlit as st
from firebase_client import firebase_login, firebase_signup, get_firestore

db = get_firestore()

# ---------------- AUTH (Firebase) ----------------

def username_exists(username: str) -> bool:
    users = db.collection("users").where("username", "==", username).get()
    return len(users) > 0
def authenticate_user(email: str, password: str):
    """
    Login existing user using Firebase Auth.
    """
    try:
        data = firebase_login(email, password)
        return {
            "email": email,
            "localId": data.get("localId"),
            "idToken": data.get("idToken")
        }
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None


def register_user(email: str, password: str):
    """
    Create a new user in Firebase Auth + optionally store profile in Firestore.
    """
    try:
        data = firebase_signup(email, password)

        # Optionally store additional user profile data in Firestore
        db.collection("users").document(data["localId"]).set({
            "email": email,
            "created_at": firestore.SERVER_TIMESTAMP
        })

        return {
            "email": email,
            "localId": data.get("localId"),
            "idToken": data.get("idToken")
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
