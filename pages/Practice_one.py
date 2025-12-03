import streamlit as st
import json
import tempfile
import pandas as pd

# THEME + SIDEBAR (NO LOGIN ENFORCEMENT)
from Theme import apply_theme, add_sidebar_navigation  

# MODEL / PROCESSING
from prosody_extractor import extract_prosodic_features
from model_loader import predict_traits_from_prosody
from database import save_interview_result

# GPT FEEDBACK GENERATION
from pages.gpt_feedback import generate_prosody_feedback, generate_text_feedback


# -------------------------------------------------
# BASE THEME + SIDEBAR
# -------------------------------------------------
apply_theme()
add_sidebar_navigation()

# -------------------------------------------------
# SAFE USER HANDLING (no crash if user is None)
# -------------------------------------------------
user_data = st.session_state.get("user") or {}
username = user_data.get("username", "Guest")


# -------------------------------------------------
# VALIDATION
# -------------------------------------------------
if "selected_question_index" not in st.session_state:
    st.error("Please select a question first.")
    st.stop()

if "role" not in st.session_state:
    st.error("Incomplete flow. Please start again.")
    st.stop()


# -------------------------------------------------
# LOAD QUESTIONS
# -------------------------------------------------
@st.cache_data
def load_questions():
    with open("data/hr_interview_questions_dataset.json", "r", encoding="utf-8") as f:
        return json.load(f)

question_bank = load_questions()

role = st.session_state.role
experience = st.session_state.experience
difficulty = st.session_state.difficulty
qmode = st.session_state.question_mode
idx = st.session_state.selected_question_index

filtered = [
    q for q in question_bank
    if q["role"].lower() == role.lower()
    and q["experience"].lower() == experience.lower()
    and q["difficulty"].lower() == difficulty.lower()
    and q["source_type"].lower() == qmode.lower()
]

questions = [q["question"] for q in filtered]
current_question = questions[idx]


# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(f"""
<h2 style='text-align:center;margin-top:10px;'>Practice Your Answer</h2>
<h4 style='text-align:center;color:#9ecbff;'>
Question {idx + 1} of {len(questions)}
</h4>
""", unsafe_allow_html=True)

# QUESTION CARD
st.markdown(f"""
<div style="
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
">
<p style="color:#bcdcff; font-size:1.2rem;">{current_question}</p>
</div>
""", unsafe_allow_html=True)


# -------------------------------------------------
# INPUT AREA
# -------------------------------------------------
st.markdown("### 🎤 Type or Record Your Answer")

col1, col2 = st.columns(2)

with col1:
    user_text = st.text_area("Type your answer:", height=180, key=f"text_ans_{idx}")

with col2:
    audio_input = st.audio_input("Or record your answer:", key=f"audio_ans_{idx}")


# -------------------------------------------------
# SAVE TEMP AUDIO
# -------------------------------------------------
def save_temp_audio(uploaded_file):
    if uploaded_file is None:
        return None

    audio_bytes = uploaded_file.getvalue()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        return tmp.name


# -------------------------------------------------
# SUBMIT ANSWER
# -------------------------------------------------
if st.button("Submit Answer", use_container_width=True):

    if not user_text and not audio_input:
        st.warning("Please type or record an answer before submitting.")
        st.stop()

    st.session_state.last_answer = user_text

    prosody_series = None
    prosody_features = {}
    trait_scores = {}

    # -------------------- VOICE ANALYSIS --------------------
    if audio_input:
        st.info("⏳ Extracting prosodic features…")

        audio_path = save_temp_audio(audio_input)
        prosody_series = extract_prosodic_features(audio_path)
        prosody_features = prosody_series.to_dict()

        st.success("🎯 Voice features extracted!")

        # Predict Traits
        trait_scores = predict_traits_from_prosody(prosody_series)

    # -------------------- DISPLAY NUMERIC SCORES --------------------
    clarity_score = trait_scores.get("Overall", 0)          # already 0–100
    confidence_score = trait_scores.get("NotStressed", 0)   # already 0–100
    fluency_score = trait_scores.get("Calm", 0)             # already 0–100

    st.markdown("## 📊 Model Trait Scores")
    st.write(f"### 🔹 Clarity: `{clarity_score:.1f}%`")
    st.write(f"### 🔹 Confidence: `{confidence_score:.1f}%`")
    st.write(f"### 🔹 Fluency: `{fluency_score:.1f}%`")

    if prosody_features:
        with st.expander("🎧 Detailed Prosodic Features"):
            st.json(prosody_features)

    # -------------------- GPT FEEDBACK --------------------
    if trait_scores:
        st.info("🧠 Generating voice-based communication feedback…")
        pf = generate_prosody_feedback(trait_scores)

        st.markdown("## 🗣️ Voice-Based Communication Feedback")
        st.write("### Summary")
        st.write(pf.get("summary", ""))

        st.write("### Strengths")
        for s in pf.get("strengths", []):
            st.write(f"- {s}")

        st.write("### Areas to Improve")
        for s in pf.get("improvements", []):
            st.write(f"- {s}")

        st.write("### Actionable Tips")
        for s in pf.get("action_items", []):
            st.write(f"- {s}")

    # Text Feedback
    if user_text:
        st.info("🧠 Analyzing your written answer…")
        tf = generate_text_feedback(user_text)

        st.markdown("## 📝 Text-Based Feedback")
        st.write("### Summary")
        st.write(tf.get("summary", ""))

        st.write("### Strengths")
        for s in tf.get("strengths", []):
            st.write(f"- {s}")

        st.write("### Improvements")
        for s in tf.get("improvements", []):
            st.write(f"- {s}")

        st.write("### Missing Points")
        for s in tf.get("missing_points", []):
            st.write(f"- {s}")

        st.write(f"### Score: **{tf.get('score', '?')}/10**")


    # -------------------- SAVE DATA (SAFE) --------------------
    save_interview_result({
        "username": username,        # SAFE FIX
        "question": current_question,
        "role": role,
        "experience": experience,
        "difficulty": difficulty,
        "clarity": clarity_score,
        "confidence": confidence_score,
        "fluency": fluency_score,
        "prosodic_features": prosody_features
    })


    # -------------------- TRACK COMPLETED --------------------
    if "completed_questions" not in st.session_state:
        st.session_state.completed_questions = set()

    st.session_state.completed_questions.add(idx)

    # NEXT QUESTION
    if idx < len(questions) - 1:
        st.success("Answer saved! Moving to the next question… ⏭️")
        st.session_state.selected_question_index = idx + 1
        st.rerun()

    else:
        st.balloons()
        st.success("🎉 You've completed all practice questions!")


# -------------------------------------------------
# BACK BUTTON
# -------------------------------------------------
if st.button("⬅ Back to Question List", use_container_width=True):
    st.switch_page("pages/Practice_Question.py")
