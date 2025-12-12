import json
import os

# Get base directory (one level up from /pages)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Build the correct path to the data file
DATA_PATH = os.path.join(BASE_DIR, "data", "hr_interview_questions_dataset.json")

# Load questions safely
with open(DATA_PATH, "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)
