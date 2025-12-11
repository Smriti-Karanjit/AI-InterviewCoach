import streamlit as st
import tempfile
import pandas as pd

# THEME + SIDEBAR
from Theme import apply_theme, add_sidebar_navigation  
from prosody_extractor import extract_prosodic_features
from model_loader import predict_traits_from_prosody
from database import save_interview_result
from pages.gpt_feedback import generate_prosody_feedback, generate_text_feedback


# -------------------------------------------------
# BASE THEME + SIDEBAR
# -------------------------------------------------
apply_theme()
add_sidebar_navigation()

# -------------------------------------------------
# SAFE USER HANDLING
# -------------------------------------------------
user_data = st.session_state.get("user") or {}
username = user_data.get("username", "Guest")


# -------------------------------------------------
# VALIDATION
# -------------------------------------------------
if "selected_question_index" not in st.session_state:
    st.error("Please select a question first.")
    st.stop()

if "filtered_questions" not in st.session_state:
    st.error("Missing question data. Please go back.")
    st.stop()


questions = st.session_state.filtered_questions
idx = st.session_state.selected_question_index

if idx >= len(questions):
    st.error("Invalid question index. Restart practice.")
    st.stop()

current_question = questions[idx]["question"]
role = st.session_state.role
experience = st.session_state.experience
difficulty = st.session_state.difficulty
qmode = st.session_state.question_mode


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
# SUBMIT ANSWER BUTTON
# -------------------------------------------------
if st.button("Submit Answer", use_container_width=True):

    if not user_text and not audio_input:
        st.warning("Please type or record an answer before submitting.")
        st.stop()

    st.session_state.last_answer = user_text

    prosody_features = {}
    trait_scores = {}

    # -------------------- VOICE ANALYSIS --------------------
    if audio_input:
        st.info("⏳ Extracting prosodic features…")
        audio_path = save_temp_audio(audio_input)
        prosody_series = extract_prosodic_features(audio_path)
        prosody_features = prosody_series.to_dict()

        st.success("🎯 Voice features extracted!")
        trait_scores = predict_traits_from_prosody(prosody_series)

    # -------------------- NUMERIC SCORES --------------------
    clarity_score = trait_scores.get("Overall", 0)
    confidence_score = trait_scores.get("NotStressed", 0)
    fluency_score = trait_scores.get("Calm", 0)

    st.markdown("## 📊 Model Trait Scores")
    st.write(f"### 🔹 Clarity: `{clarity_score:.1f}%`")
    st.write(f"### 🔹 Confidence: `{confidence_score:.1f}%`")
    st.write(f"### 🔹 Fluency: `{fluency_score:.1f}%`")

    if prosody_features:
        with st.expander("🎧 Detailed Prosodic Features"):
            st.json(prosody_features)

    # -------------------- GPT FEEDBACK --------------------
    if trait_scores:
        pf = generate_prosody_feedback(trait_scores)
        st.markdown("## 🗣️ Voice-Based Communication Feedback")
        st.write("### Summary")
        st.write(pf.get("summary", ""))
        st.write("### Strengths")
        st.write("\n".join(f"- {s}" for s in pf.get("strengths", [])))
        st.write("### Areas to Improve")
        st.write("\n".join(f"- {s}" for s in pf.get("improvements", [])))
        st.write("### Actionable Tips")
        st.write("\n".join(f"- {s}" for s in pf.get("action_items", [])))

    if user_text:
        tf = generate_text_feedback(user_text)
        st.markdown("## 📝 Text-Based Feedback")
        st.write("### Summary")
        st.write(tf.get("summary", ""))
        st.write("### Strengths")
        st.write("\n".join(f"- {s}" for s in tf.get("strengths", [])))
        st.write("### Improvements")
        st.write("\n".join(f"- {s}" for s in tf.get("improvements", [])))
        st.write("### Missing Points")
        st.write("\n".join(f"- {s}" for s in tf.get("missing_points", [])))
        st.write(f"### Score: **{tf.get('score', '?')}/10**")

    # -------------------- SAVE TO DB --------------------
    save_interview_result({
        "username": username,
        "question": current_question,
        "role": role,
        "experience": experience,
        "difficulty": difficulty,
        "clarity": clarity_score,
        "confidence": confidence_score,
        "fluency": fluency_score,
        "prosodic_features": prosody_features
    })

    # -------------------- NEXT QUESTION --------------------
    if idx + 1 < len(questions):
        st.session_state.selected_question_index = idx + 1
        st.rerun()
    else:
        st.balloons()
        st.success("🎉 You've completed all questions!")


# -------------------------------------------------
# BACK BUTTON
# -------------------------------------------------
if st.button("⬅ Back to Question List", use_container_width=True):
    st.switch_page("pages/Practice_Question.py")
