import os
import requests
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

# ---------- AUTH CONFIG ----------
API_KEY = os.getenv("FIREBASE_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing FIREBASE_API_KEY in .env")

SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
LOGIN_URL  = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

# ---------- FIRESTORE CONFIG ----------
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path or not os.path.exists(cred_path):
    raise RuntimeError("Firebase credentials JSON not found.")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------- AUTH HELPERS ----------
def firebase_signup(email, password):
    payload = {"email": email, "password": password, "returnSecureToken": True}
    resp = requests.post(SIGNUP_URL, json=payload)
    data = resp.json()
    if resp.status_code != 200:
        raise ValueError(data.get("error", {}).get("message"))
    return data

def firebase_login(email, password):
    payload = {"email": email, "password": password, "returnSecureToken": True}
    resp = requests.post(LOGIN_URL, json=payload)
    data = resp.json()
    if resp.status_code != 200:
        raise ValueError(data.get("error", {}).get("message"))
    return data

def get_firestore():
    return db
