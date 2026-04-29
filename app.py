import streamlit as st
import re

from modules.parser import extract_text
from modules.ai_handler import analyze_resume
from modules.utils import clean_text, validate_ai_output
from modules.jd_matcher import calculate_match
from modules.keyword_extractor import load_skills, extract_keywords
from modules.pdf_generator import generate_pdf
from config import SKILLS_FILE


# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer")


# --- INPUTS ---
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
jd_text = st.text_area("Paste Job Description (Optional)")


# --- LOAD SKILLS ---
skills_list = load_skills(SKILLS_FILE)


# --- FUNCTION: EXTRACT JD SKILLS ---
def extract_jd_skills(jd_text):
    jd_text = jd_text.lower()

    skill_pool = [
        "python", "django", "flask", "pyramid",
        "orm", "sql", "database",
        "javascript", "html", "css",
        "api", "backend",
        "debugging", "testing",
        "security", "performance"
    ]

    return list(set([skill for skill in skill_pool if skill in jd_text]))


# --- MAIN BUTTON ---
if st.button("Analyze Resume"):

    if not uploaded_file:
        st.error("Please upload a resume.")
        st.stop()

    # --- STEP 1: EXTRACT TEXT ---
    raw_text = extract_text(uploaded_file)

    if not raw_text:
        st.error("Could not extract text from the PDF.")
        st.stop()

    # --- STEP 2: CLEAN TEXT ---
    cleaned_text = clean_text(raw_text)

    # --- STEP 3: LIMIT JD SIZE ---
    combined_text = cleaned_text
    if jd_text:
        combined_text += "\n\nJob Description:\n" + jd_text[:1000]

    # --- STEP 4: AI ANALYSIS ---
    with st.spinner("Analyzing resume..."):
        ai_result = analyze_resume(combined_text)

    if "error" in ai_result:
        st.error(f"AI Error: {ai_result['error']}")
        st.stop()

    # --- STEP 5: VALIDATE OUTPUT ---
    data = validate_ai_output(ai_result)

    # --- STEP 6: KEYWORDS ---
    keywords = extract_keywords(cleaned_text, skills_list)

    # --- STEP 7: JD MATCH ---
    match_score = calculate_match(cleaned_text, jd_text) if jd_text else None

    # --- STEP 8: DYNAMIC JD SKILL MATCH (REAL FIX) ---
    if jd_text:
        jd_skills = extract_jd_skills(jd_text)
        resume_lower = cleaned_text.lower()

        missing = [skill for skill in jd_skills if skill not in resume_lower]

        if missing:
            data["missing_skills"] = missing[:3]

    # --- STEP 9: CLEAN WEAKNESSES ---
    if any("limited experience" in w.lower() for w in data["weaknesses"]):
        data["weaknesses"] = [
            "Lacks quantified achievements in projects",
            "Could improve clarity and impact in descriptions"
        ]

    # --- DISPLAY RESULTS ---

    st.subheader("📊 Overall Score")

    score = data["score"]

    if score >= 80:
        st.success(f"Score: {score}/100")
    elif score >= 60:
        st.warning(f"Score: {score}/100")
    else:
        st.error(f"Score: {score}/100")

    # --- SUMMARY ---
    st.subheader("🧾 Summary")
    st.write(data["summary"])

    # --- STRENGTHS & WEAKNESSES ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Strengths")
        for s in data["strengths"]:
            st.write(f"- {s}")

    with col2:
        st.subheader("❌ Weaknesses")
        for w in data["weaknesses"]:
            st.write(f"- {w}")

    # --- MISSING SKILLS ---
    st.subheader("📉 Missing Skills")
    for m in data["missing_skills"]:
        st.write(f"- {m}")

    # --- SUGGESTIONS ---
    st.subheader("💡 Suggestions")
    for s in data["suggestions"]:
        st.write(f"- {s}")

    # --- SECTION SCORES ---
    st.subheader("📌 Section Scores")
    for key, value in data["section_scores"].items():
        st.write(f"{key.capitalize()}: {value}")

    # --- KEYWORDS ---
    st.subheader("🔑 Detected Keywords")
    if keywords:
        st.write(", ".join(keywords))
    else:
        st.write("No keywords detected")

    # --- JD MATCH ---
    if match_score is not None:
        st.subheader("📈 Job Match Score")
        st.metric("Match %", f"{match_score}%")

    # --- PDF GENERATION ---
    pdf_path = generate_pdf(data)

    if pdf_path:
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download Report",
                data=f,
                file_name="resume_analysis.pdf",
                mime="application/pdf"
            )