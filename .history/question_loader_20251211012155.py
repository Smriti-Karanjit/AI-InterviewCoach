import os
import json

# Get PROJECT ROOT (parent of this file)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# FIX: data folder inside project root
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

print("Loading data from:", DATA_DIR)

ROLE_TO_FILE = {
    "qa analyst": "qa_analyst.json",
    "data scientist": "data_scientist.json",
    "marketing associate": "marketing_associate.json",
    "devops engineer": "devops_engineer.json",
    "hr specialist": "hr_specialist.json",
    "software engineer": "software_engineer.json",
    "product manager": "product_manager.json",
    "ux designer": "ux_designer.json",
}

def load_questions_for_role(role: str):
    role = role.lower().strip()

    if role not in ROLE_TO_FILE:
        raise ValueError(f"No dataset found for role: {role}")

    filepath = os.path.join(DATA_DIR, ROLE_TO_FILE[role])

    print("Looking for file:", filepath)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"JSON not found at: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
