from groq import Groq
import json

# Your GROQ API key
client = Groq(api_key="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")

# -------------------------------------------------------------
#  FEEDBACK BASED ON PROSODIC BEHAVIORAL TRAIT SCORES
# -------------------------------------------------------------
def generate_prosody_feedback(predictions: dict):
    """
    Takes prosodic trait predictions from your model and returns feedback text.
    Helps summarize clarity, fluency, confidence, stress level, etc.
    """

    if not predictions:
        return None

    # Convert dict → readable bullet list
    scores_text = "\n".join([f"{trait}: {value:.3f}" for trait, value in predictions.items()])

    prompt = f"""
    You are an expert AI interview coach.

    Here are the behavioral trait scores predicted from the candidate's voice:

    {scores_text}

    Based on these scores, provide structured feedback in JSON format with:
    - "summary": 2–3 sentence summary of their communication style
    - "strengths": list of 3 strengths
    - "improvements": list of 3 improvements
    - "action_items": list of 3 actionable suggestions

    The tone should be supportive, professional, and interview-oriented.
    Only return valid JSON.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    # Try to parse JSON
    try:
        return json.loads(content)
    except:
        return {"summary": content}  # fallback if not JSON


# -------------------------------------------------------------
#  FEEDBACK BASED ON TEXT ANSWER
# -------------------------------------------------------------
def generate_text_feedback(user_text: str):
    """
    Uses GROQ to analyze the user's written answer.
    Returns summary, strengths, improvements, missing points, and score.
    """

    if not user_text or len(user_text.strip()) == 0:
        return None

    prompt = f"""
    You are an expert technical and HR interview coach.

    Analyze the following interview answer:

    {user_text}

    Return your output ONLY as JSON with the fields:
    - "summary"
    - "strengths" (list)
    - "improvements" (list)
    - "missing_points" (list)
    - "score" (integer 1–10)

    Keep the tone supportive and concise.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {"summary": content}
