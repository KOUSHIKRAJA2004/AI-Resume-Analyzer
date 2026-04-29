import requests
import re
from config import MAX_INPUT_CHARS, OLLAMA_MODEL


def call_ollama(prompt: str) -> str:
    """
    Call Ollama API
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 800
            }
        }
    )

    result = response.json()
    return result.get("response", "").strip()


def parse_output(text: str) -> dict:
    """
    Convert structured text output into JSON-like dict
    """
    try:
        data = {
            "score": 70,
            "summary": "",
            "strengths": [],
            "weaknesses": [],
            "missing_skills": [],
            "suggestions": [],
            "section_scores": {
                "education": 70,
                "experience": 70,
                "skills": 70,
                "projects": 70
            }
        }

        # --- Score ---
        match = re.search(r"Score:\s*(\d+)", text)
        if match:
            data["score"] = int(match.group(1))

        # --- Summary ---
        summary = re.search(r"Summary:\n(.+?)\n\n", text, re.DOTALL)
        if summary:
            data["summary"] = summary.group(1).strip()

        # --- Extract list helper ---
        def extract_list(section):
            match = re.search(rf"{section}:\n(.*?)\n\n", text, re.DOTALL)
            if match:
                return [
                    line.strip("- ").strip()
                    for line in match.group(1).split("\n")
                    if line.strip()
                ]
            return []

        data["strengths"] = extract_list("Strengths")
        data["weaknesses"] = extract_list("Weaknesses")
        data["missing_skills"] = extract_list("Missing Skills")
        data["suggestions"] = extract_list("Suggestions")

        # --- Section scores ---
        for key in data["section_scores"]:
            match = re.search(rf"{key.capitalize()}:\s*(\d+)", text)
            if match:
                data["section_scores"][key] = int(match.group(1))

        return data

    except:
        return None


def analyze_resume(resume_text: str) -> dict:
    """
    Main function
    """

    prompt = f"""
You are an ATS resume evaluator.

Analyze the resume and respond EXACTLY in this format:

Score: <number between 60 and 95>

Summary:
<2-3 lines>

Strengths:
- point 1
- point 2
- point 3

Weaknesses:
- point 1
- point 2

Missing Skills:
- skill 1
- skill 2
- skill 3

Suggestions:
- suggestion 1
- suggestion 2
- suggestion 3

Section Scores:
Education: <number>
Experience: <number>
Skills: <number>
Projects: <number>

Rules:
- Do not skip any section
- Do not add extra explanation

Resume:
{resume_text[:MAX_INPUT_CHARS]}
"""

    try:
        # --- First attempt ---
        raw_text = call_ollama(prompt)
        data = parse_output(raw_text)

        # --- Retry if needed ---
        if data is None or not data["summary"]:
            raw_text = call_ollama(prompt)
            data = parse_output(raw_text)

        # --- Final fallback ---
        if data is None or not data["summary"]:
            return {
                "score": 75,
                "summary": "Resume analysis could not be fully generated.",
                "strengths": ["Relevant technical skills present"],
                "weaknesses": ["Insufficient structured output from model"],
                "missing_skills": ["Cloud platforms", "System design"],
                "suggestions": ["Retry analysis for better results"],
                "section_scores": {
                    "education": 75,
                    "experience": 75,
                    "skills": 75,
                    "projects": 75
                }
            }

        return data

    except Exception as e:
        return {"error": str(e)}