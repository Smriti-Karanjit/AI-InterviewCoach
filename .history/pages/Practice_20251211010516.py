import streamlit as st
import base64, os
from Theme import apply_theme, add_sidebar_navigation, require_login

# Session init
if "user" not in st.session_state:
    st.session_state.user = None

apply_theme()
require_login()
add_sidebar_navigation()

st.markdown("<h2 style='text-align:center;'>Practice Mode</h2>", unsafe_allow_html=True)

roles = [
    {"title":"QA Analyst","subtitle":"Testing","image":"QA.webp"},
    {"title":"Data Scientist","subtitle":"Machine Learning","image":"ds.jpg"},
    {"title":"Marketing Associate","subtitle":"Marketing","image":"ma.jpg"},
    {"title":"DevOps Engineer","subtitle":"Infrastructure","image":"devops.webp"},
    {"title":"HR Specialist","subtitle":"People Ops","image":"HR.webp"},
    {"title":"Software Engineer","subtitle":"Development","image":"se.webp"},
    {"title":"Product Manager","subtitle":"Strategy","image":"PM.png"},
    {"title":"UX Designer","subtitle":"Design","image":"UX.png"},
    {"title":"Coming Soon","subtitle":"New Role","image":"coming.jpg"}
]

def mime_type(name):
    ext = name.split(".")[-1].lower()
    return {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
    }.get(ext, "image/jpeg")

def get_b64(path):
    full = os.path.join("assets/roles", path)
    if not os.path.exists(full):
        return ""
    return base64.b64encode(open(full, "rb").read()).decode()

cols = st.columns(3)

for i, r in enumerate(roles):

    with cols[i % 3]:

        container = st.container()  # <- CARD + BUTTON inside same width container

        img = get_b64(r["image"])
        mime = mime_type(r["image"])
        bg = f"linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)), url(data:{mime};base64,{img})"

        # -----------------------------
        # CARD
        # -----------------------------
        container.markdown(
            f"""
            <div style="
                height:170px;
                background-image:{bg};
                background-size:cover;
                background-position:center;
                border-radius:14px;
                padding:14px;
                display:flex;
                flex-direction:column;
                justify-content:flex-end;
                border:1px solid rgba(0,191,255,0.35);
                margin-bottom:6px;
            ">
                <div style="font-size:1.2rem;color:white;font-weight:700;">{r['title']}</div>
                <div style="color:#ccc;">{r['subtitle']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # -----------------------------
        # BUTTON (auto matches card width)
        # -----------------------------
        if container.button(r["title"], key=f"btn_{i}", use_container_width=True):
            st.session_state.role = r["title"]
            st.switch_page("pages/Practice_experience.py")
