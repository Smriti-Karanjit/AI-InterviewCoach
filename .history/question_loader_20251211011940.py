import os
import json

# FORCE the correct project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # question_loader.py location
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Debug path check
print("Loading data from:", DATA_DIR)

ROLE_TO_FILE = {
    "data scientist": "data_scientist.json",
    "devops engineer": "devops_engineer.json",
    "hr specialist": "hr_specialist.json",
    "marketing associate": "marketing_associate.json",
    "product manager": "product_manager.json",
    "qa analyst": "qa_analyst.json",
    "software engineer": "software_engineer.json",
    "ux designer": "ux_designer.json",
}

def load_questions_for_role(role: str):
    role = role.lower().strip()

    if role not in ROLE_TO_FILE:
        raise ValueError(f"No dataset found for role: {role}")

    filepath = os.path.join(DATA_DIR, ROLE_TO_FILE[role])

    print("Looking for file:", filepath)  # debug print

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Role file not found at: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
