import streamlit as st

# Session init (must be first)
if "user" not in st.session_state:
    st.session_state.user = None

from Theme import apply_theme, add_sidebar_navigation, require_login
import base64, os

apply_theme()
require_login()
add_sidebar_navigation()

st.markdown("<h2 style='text-align:center;'>Practice Mode</h2>", unsafe_allow_html=True)

roles = [
    {"title":"QA Analyst","subtitle":"Testing","image":"QA.webp"},
    {"title":"Data Scientist","subtitle":"Machine Learning","image":"ds.jpg"},
    {"title":"Software Engineer","subtitle":"Developer","image":"se.webp"},
    {"title":"Product Manager","subtitle":"Strategy","image":"PM.png"},
]

def get_b64(path):
    full = os.path.join("assets/roles", path)
    if not os.path.exists(full): return ""
    return base64.b64encode(open(full,"rb").read()).decode()

cols = st.columns(2)

for i, r in enumerate(roles):
    img = get_b64(r["image"])
    bg = f"linear-gradient(rgba(0,0,0,.6), rgba(0,0,0,.6)), url(data:image/png;base64,{img})"
    with cols[i % 2]:
        st.markdown(
            f"""
            <a href="?role={r['title']}" style="text-decoration:none;">
                <div style="
                    height:170px;
                    background-image:{bg};
                    border-radius:14px;
                    padding:14px;
                    margin:10px;
                    display:flex;
                    flex-direction:column;
                    justify-content:flex-end;
                    border:1px solid rgba(0,191,255,0.35);">
                    <div style="font-size:1.2rem;color:white;">{r['title']}</div>
                    <div style="color:#ccc;">{r['subtitle']}</div>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

params = st.query_params
if "role" in params:
    st.session_state.role = params["role"]
    st.query_params.clear()
    st.switch_page("pages/Practice_experience.py")
