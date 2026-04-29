def load_skills(file_path: str) -> list:
    """
    Load skills from a text file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            skills = [line.strip().lower() for line in f if line.strip()]
        return skills
    except Exception as e:
        print(f"Error loading skills: {e}")
        return []


def extract_keywords(text: str, skills_list: list) -> list:
    """
    Extract matching skills from resume text.
    """
    if not text:
        return []

    text_lower = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text_lower:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))