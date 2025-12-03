import bcrypt
from supabase import create_client
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL,SUPABASE_KEY)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str,password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"),password_hash.encode("utf-8"))

def create_user(email: str, username: str, password:str):
    password_hash=hash_password(password)
    
    result=supabase.table("users").insert({
        "email":email,
        "username":username,
        "password_hash":password_hash
    }).execute()
    return result

def get_user_by_username(username: str):
    try:
        result = (
            supabase.table("users")
            .select("*")
            .eq("username", username)
            .execute()
        )

        # If no rows returned → username does NOT exist
        if not result.data:
            return None

        # Otherwise return the first row
        return result.data[0]

    except Exception as e:
        print("Supabase error:", e)
        return None
    
def authenticate_user(username: str, password: str):
    try:
        result = (
            supabase.table("users")
            .select("*")
            .eq("username", username)
            .execute()
        )

        if not result.data:
            return None

        user = result.data[0]

        if verify_password(password, user["password_hash"]):
            return user

        return None

    except Exception as e:
        print("Auth error:", e)
        return None

def save_interview_result(data: dict):
    return supabase.table("interview_results").insert(data).execute()