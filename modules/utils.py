import re


def clean_text(text: str) -> str:
    """
    Clean extracted resume text.
    """
    if not text:
        return ""

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove non-ASCII characters (optional)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    return text.strip()


def validate_ai_output(data: dict) -> dict:
    """
    Ensure AI output has required fields and safe defaults.
    """

    default_structure = {
        "score": 0,
        "summary": "",
        "strengths": [],
        "weaknesses": [],
        "missing_skills": [],
        "suggestions": [],
        "section_scores": {
            "education": 0,
            "experience": 0,
            "skills": 0,
            "projects": 0
        }
    }

    if not isinstance(data, dict):
        return default_structure

    # Ensure keys exist
    for key in default_structure:
        if key not in data:
            data[key] = default_structure[key]

    # Validate score range
    try:
        data["score"] = int(data.get("score", 0))
        if data["score"] < 0 or data["score"] > 100:
            data["score"] = 0
    except:
        data["score"] = 0

    # Ensure lists
    for key in ["strengths", "weaknesses", "missing_skills", "suggestions"]:
        if not isinstance(data.get(key), list):
            data[key] = []

    # Ensure section_scores structure
    if "section_scores" not in data or not isinstance(data["section_scores"], dict):
        data["section_scores"] = default_structure["section_scores"]

    return data