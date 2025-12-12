import json
import os
import streamlit as st

DATA_DIR = "data"

# Mapping UI role names to the correct JSON filenames
ROLE_FILE_MAP = {
    "QA Analyst": "qa_analyst.json",
    "Data Scientist": "data_scientist.json",
    "Marketing Associate": "marketing_associate.json",
    "DevOps Engineer": "devops_engineer.json",
    "HR Specialist": "hr_specialist.json",
    "Software Engineer": "software_engineer.json",
    "Product Manager": "product_manager.json",
    "UX Designer": "ux_designer.json",
}


@st.cache_data
def load_questions_for_role(role: str):
    """
    Loads the questions for the selected role.
    Only loads the relevant JSON file.
    """

    if role not in ROLE_FILE_MAP:
        raise ValueError(f"No dataset available for role: {role}")

    filename = ROLE_FILE_MAP[role]
    filepath = os.path.join(DATA_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset file not found: {filepath}. "
            "Make sure the JSON file exists inside the /data folder."
        )

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
