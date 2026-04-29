from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_jd(jd_text: str) -> str:
    """
    Remove irrelevant HR/noise content from JD
    """
    jd_text = jd_text.lower()

    remove_words = [
        "salary", "benefits", "location", "schedule",
        "education", "experience", "job type",
        "day shift", "full-time", "permanent",
        "commute", "relocate"
    ]

    for word in remove_words:
        jd_text = jd_text.replace(word, "")

    return jd_text


def skill_match_score(resume_text: str, jd_text: str) -> float:
    """
    Match based on important technical skills
    """
    skills = [
        "python", "flask", "django", "fastapi",
        "sql", "api", "backend", "javascript",
        "html", "css", "docker", "git"
    ]

    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    jd_skills = [s for s in skills if s in jd_text]
    matched = [s for s in jd_skills if s in resume_text]

    if not jd_skills:
        return 50.0  # neutral score

    return (len(matched) / len(jd_skills)) * 100


def calculate_match(resume_text: str, jd_text: str) -> float:
    """
    Combine TF-IDF similarity + skill-based matching
    """

    if not jd_text.strip():
        return 0.0

    # --- Clean JD ---
    jd_text = clean_jd(jd_text)

    # --- TF-IDF Similarity ---
    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    tfidf_score = similarity * 100

    # --- Skill-based Score ---
    skill_score = skill_match_score(resume_text, jd_text)

    # --- Final Combined Score ---
    final_score = (0.7 * skill_score) + (0.3 * tfidf_score)

    # --- Clamp to realistic range ---
    final_score = max(30, min(95, final_score))

    return round(final_score, 2)