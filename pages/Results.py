import streamlit as st
import json
import pandas as pd
from database import fetch_user_results
from Theme import apply_theme, add_sidebar_navigation, require_login

# -------------------- APPLY THEME --------------------
apply_theme()
require_login()
add_sidebar_navigation()

st.set_page_config(page_title="📊 Results Summary")

st.markdown("<h2 style='text-align:center;margin-top:10px;'>Your Practice Results</h2>", 
            unsafe_allow_html=True)

username = st.session_state.user["username"]
results = fetch_user_results(username)

if not results:
    st.info("No results yet. Practice first!")
    st.stop()

df = pd.DataFrame(results)

# -------- Parse JSON safely --------
def safe_json(val):
    if isinstance(val, str):
        try:
            return json.loads(val)
        except:
            return {}
    return val

df["traits"] = df["traits"].apply(safe_json)
df["prosodic_features"] = df["prosodic_features"].apply(safe_json)

# ============================================================
# ⭐ HORIZONTAL BAR STYLE (CSS)
# ============================================================
st.markdown("""
<style>
.score-bar-container {
    width: 100%;
    background-color: rgba(255,255,255,0.15);
    border-radius: 8px;
    margin-bottom: 8px;
}

.score-bar-fill {
    height: 22px;
    border-radius: 8px;
    background: linear-gradient(90deg, #00bfff, #0088cc);
    text-align: right;
    padding-right: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #ffffff;
}
.score-label {
    margin-bottom: 4px;
    font-size: 1rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# ⭐ SHOW HORIZONTAL BARS FOR EACH QUESTION
# ============================================================

for idx, row in df.iterrows():

    with st.expander(f"🔍 Question {idx+1}: {row['question'][:70]}…"):

        clarity = round(row["clarity"] * 100, 1)
        confidence = round(row["confidence"] * 100, 1)
        fluency = round(row["fluency"] * 100, 1)

        # ---------- CLARITY ----------
        st.markdown("<div class='score-label'>Clarity</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='score-bar-container'>
                <div class='score-bar-fill' style='width:{clarity}%'>
                    {clarity}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ---------- CONFIDENCE ----------
        st.markdown("<div class='score-label'>Confidence</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='score-bar-container'>
                <div class='score-bar-fill' style='width:{confidence}%'>
                    {confidence}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ---------- FLUENCY ----------
        st.markdown("<div class='score-label'>Fluency</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='score-bar-container'>
                <div class='score-bar-fill' style='width:{fluency}%'>
                    {fluency}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ---------- RAW DETAILS ----------
        st.write("### 🧠 Trait Scores")
        st.json(row["traits"])

        st.write("### 🎧 Prosodic Features")
        st.json(row["prosodic_features"])
