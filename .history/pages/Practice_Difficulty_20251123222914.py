import streamlit as st
from Theme import apply_theme, add_sidebar_navigation

apply_theme()
add_sidebar_navigation()

if "role" not in st.session_state or st.session_state.role is None:
    st.error("Please select a role first.")
    st.stop()
if "experience" not in st.session_state or st.session_state.experience is None:
    st.error("Please select experience level first.")
    st.stop()

role = st.session_state.role
exp = st.session_state.experience

# ===========================
# HEADER
# ===========================
st.markdown(f"""
<h2 style='text-align:center; margin-top:15px; font-size:36px;'>
    Role: {role}
</h2>
<h4 style='text-align:center; margin-top:-10px; color:#9ecbff;'>
    Experience: {exp}
</h4>
""", unsafe_allow_html=True)


# ===========================
# GLOBAL STYLES
# ===========================
st.markdown("""
<style>

.section-box {
    background: rgba(0, 40, 90, 0.22);
    border: 1px solid rgba(0,191,255,0.20);
    border-radius: 16px;
    padding: 28px;
    margin-top: 25px;
    box-shadow: 0 0 25px rgba(0,191,255,0.12);
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 20px;
    text-align: center;
    color: #d6ecff;
}

/* Manual wrapper to center content safely (NOT overriding Streamlit columns) */
.column-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

/* Unselected Button */
.card-btn-normal > button {
    background: rgba(0, 80, 140, 0.30) !important;
    border: 1px solid rgba(0,191,255,0.30) !important;
    color: #d6ecff !important;
    border-radius: 14px !important;
    padding: 14px !important;
    width: 220px !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    transition: 0.25s ease-in-out !important;
}

.card-btn-normal > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 22px rgba(0,191,255,0.5);
}

/* Selected Button */
.card-btn-selected > button {
    background: linear-gradient(145deg, #00bfff, #0099d6) !important;
    color: #001020 !important;
    border-radius: 14px !important;
    padding: 14px !important;
    width: 220px !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 0 35px rgba(0,191,255,0.85) !important;
}

/* Subtitle */
.card-sub {
    text-align:center;
    color:#d4e9ff;
    opacity:0.75;
    font-size:0.85rem;
    margin-top:10px;
    min-height: 40px;
}

</style>
""", unsafe_allow_html=True)



# ===========================
# DIFFICULTY SECTION
# ===========================
st.markdown("<div class='section-title'>Select difficulty level</div>", unsafe_allow_html=True)

difficulties = ["Easy", "Medium", "Hard"]

if "difficulty" not in st.session_state:
    st.session_state.difficulty = None

cols = st.columns(3)

for i, diff in enumerate(difficulties):
    with cols[i]:

        selected = st.session_state.difficulty == diff

        btn = st.button(diff, key=f"diff_{diff}")

        # Apply style AFTER the button (Streamlit safe)
        class_name = "card-btn-selected" if selected else "card-btn-normal"
        st.markdown(f"<div class='{class_name}'></div>", unsafe_allow_html=True)

        if btn:
            st.session_state.difficulty = diff

st.markdown("</div>", unsafe_allow_html=True)




# ===========================
# QUESTION MODE SECTION
# ===========================

st.markdown("<div class='section-title'>Select question mode</div>", unsafe_allow_html=True)

question_modes = [
    ("STAR-Based", "Situation · Task · Action · Result"),
    ("Open-Ended", "Explain · Describe · Tell me about…"),
    ("Behavioral", "Past Experiences · Teamwork · Conflict"),
    ("Situational", "Future Scenarios · Hypothetical Problems")
]

if "question_mode" not in st.session_state:
    st.session_state.question_mode = None

cols = st.columns(4)

for i, (mode, subtitle) in enumerate(question_modes):
    with cols[i]:

        clicked = st.button(mode, key=f"mode_{mode}")
        selected = st.session_state.question_mode == mode

        class_name = "card-btn-selected" if selected else "card-btn-normal"

        st.markdown(f"<div class='{class_name}'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-sub'>{subtitle}</div>", unsafe_allow_html=True)

        if clicked:
            st.session_state.question_mode = mode

st.markdown("</div>", unsafe_allow_html=True)




# ===========================
# START BUTTON
# ===========================
st.markdown("<br><br>", unsafe_allow_html=True)

difficulty = st.session_state.get("difficulty")
qmode = st.session_state.get("question_mode")

if difficulty and qmode:
    st.success(f"Selected: **{difficulty} difficulty** · **{qmode} questions**")

    start = st.button("🚀 Start Practice", use_container_width=True)

    if start:
        st.session_state.question_index = 0
        st.switch_page("pages/Practice_Question.py")

else:
    st.info("Select both difficulty and question mode to continue.")

