import streamlit as st

def add_top_nav():
    """
    Displays a clean sticky top navigation bar for logged-in users.
    Hidden on login and signup pages.
    """

    # Do not show navbar if user is not logged in.
    if "user" not in st.session_state or st.session_state.user is None:
        return

    # --- STYLES ---
    st.markdown(
        """
        <style>
        .top-nav {
            position: sticky;
            top: 0;
            width: 100%;
            z-index: 999;
            background: rgba(0, 18, 48, 0.85);
            backdrop-filter: blur(10px);
            padding: 12px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.12);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .nav-links a {
            margin-right: 22px;
            text-decoration: none;
            font-size: 1.05rem;
            font-weight: 500;
            color: #e0f7ff !important;
        }

        .nav-links a:hover {
            color: #00c4ff !important;
        }

        .logout-btn {
            padding: 6px 18px;
            background: rgba(255,255,255,0.08);
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.2);
            color: #e0f7ff;
            cursor: pointer;
        }
        .logout-btn:hover {
            background: rgba(255,255,255,0.18);
            border-color: #00c4ff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- HTML NAV BAR ---
    st.markdown(
        """
        <div class="top-nav">
            <div class="nav-links">
                <a href="/app" target="_self">Home</a>
                <a href="/pages/Practice" target="_self">Practice</a>
                <a href="/pages/History" target="_self">History</a>
                <a href="/pages/Profile" target="_self">Profile</a>
            </div>
            <button class="logout-btn" onclick="window.location.href='?logout=true'">Logout</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- HANDLE LOGOUT ---
    if st.query_params.get("logout"):
        # clear session
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.user = None
        st.query_params.clear()
        st.experimental_rerun()


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
