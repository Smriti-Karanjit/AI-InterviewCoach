import streamlit as st

# ---------------- NO LOGIN PROTECTION (DISABLED) ----------------
def require_login():
    # NO AUTH CHECK ANYMORE
    # You said: “I just want my app to work without login logic”
    pass

# ---------------- CLEAN USER DICT ----------------
def sanitize_user(user: dict):
    clean = {}
    for key, value in user.items():
        clean[key] = "" if value is None else value
    return clean

# ---------------- GLOBAL THEME ----------------
def apply_theme():
    st.set_page_config(layout="wide")

    st.markdown("""
    <style>

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001933, #002447, #003366) !important;
        padding: 22px !important;
        width: 260px !important;
    }

    [data-testid="stSidebarNav"] a {
        background: rgba(255,255,255,0.07) !important;
        padding: 12px !important;
        margin-bottom: 10px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0,191,255,0.25) !important;
        color: #e0f7ff !important;
        transition: 0.15s ease-in-out;
        font-size: 1rem !important;
        text-decoration: none !important;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: rgba(0,191,255,0.25) !important;
        border-color: rgba(0,191,255,0.7) !important;
        transform: translateX(6px);
    }

    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(0,191,255,0.35) !important;
        border: 1px solid rgba(0,191,255,0.8) !important;
        font-weight: 700 !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #001230 !important;
    }

    html, body, p, span, div {
        color: #e0f7ff !important;
        font-family: "Segoe UI", sans-serif !important;
    }

    /* Button styling (YOUR ORIGINAL LOOK) */
    .stButton > button {
        background: rgba(255,255,255,0.06) !important;
        backdrop-filter: blur(10px);
        color: #e9f6ff !important;
        border: 1px solid rgba(0,191,255,0.40) !important;
        border-radius: 12px !important;
        padding: 10px 18px !important;
        font-weight: 600 !important;
        transition: 0.2s ease-in-out;
    }

    .stButton > button:hover {
        background: rgba(0,191,255,0.15) !important;
        border-color: rgba(0,191,255,0.7) !important;
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    </style>
    """, unsafe_allow_html=True)

# ---------------- CUSTOM SIDEBAR ----------------
def add_sidebar_navigation():
    user = st.session_state.get("user")

    with st.sidebar:

        # Username header
        if user and "username" in user:
            st.markdown(
                f"""
                <div style="
                    padding: 14px;
                    background: rgba(0,191,255,0.15);
                    border: 1px solid rgba(0,191,255,0.35);
                    border-radius: 12px;
                    margin-bottom: 25px;
                    text-align:center;
                    font-weight:600;
                    font-size: 1.05rem;">
                    👋 Welcome, {user['username']}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Navigation
        st.page_link("pages/Practice.py", label="🎙️ Practice Mode")
        st.page_link("pages/Progress.py", label="📈 Progress Tracker")
        st.page_link("pages/Profile.py", label="⚙️ Profile Setup")

        st.markdown("<div style='height: 220px;'></div>", unsafe_allow_html=True)

        if user:
            if st.button("Logout", use_container_width=True):
                st.session_state.user = None
                st.switch_page("app.py")
