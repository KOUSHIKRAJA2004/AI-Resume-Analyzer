# 📄 AI Resume Analyzer

## Overview
This project is a simple AI-powered resume analyzer built to evaluate resumes and provide structured feedback. The goal was not just to use AI, but to build a **working, reliable system** that can handle imperfect AI outputs and still deliver meaningful results. 

The application allows users to upload a resume (PDF), optionally provide a job description, and receive:
* an overall score
* strengths and weaknesses
* missing skills
* improvement suggestions
* a short profile summary

---

## 🔗 Links
* **Demo Video:** [Watch on Google Drive](https://drive.google.com/file/d/1692YLnmsiueSkmx5Rj9KeDDEaY4U3gS7/view?usp=sharing)
* **GitHub Repository:** [KOUSHIKRAJA2004/AI-Resume-Analyzer](https://github.com/KOUSHIKRAJA2004/AI-Resume-Analyzer)

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/KOUSHIKRAJA2004/AI-Resume-Analyzer
cd AI-Resume-Analyzer
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Install Ollama 
Download and install Ollama from: https://ollama.com 
Then pull the model:
```bash
ollama pull llama3.2
```

### 6. Run the application
```bash
streamlit run app.py
```

---

## 🧠 Architecture / Flow
The system follows a simple but structured pipeline: 

1. **Upload Resume**
   * User uploads a PDF file
2. **Text Extraction**
   * Resume text is extracted and cleaned
3. **AI Analysis (Ollama)**
   * The cleaned text is sent to a local LLM
   * The model returns structured text (not raw JSON)
4. **Parsing Layer**
   * The output is parsed into structured fields
   * This avoids JSON failures common with local models
5. **Validation Layer**
   * Missing or weak outputs are corrected
   * Ensures consistent structure
6. **JD Matching (Optional)**
   * Resume is compared with job description
   * Uses TF-IDF + skill-based matching
7. **Result Display**
   * Results shown in UI (Streamlit)
   * PDF report can be downloaded

---

## 🤖 AI Tools / Models Used
* **Ollama (Local LLM Runtime)**
* Model: `llama3.2`

Reason for choosing local LLM:
* No API quota issues
* Works offline
* More control over behavior

---

## 📝 Prompt Used
The model is guided using a structured format prompt like:
```text
You are an ATS resume evaluator.

Analyze the resume and respond EXACTLY in this format:

Score: <number>

Summary:
<2-3 lines>

Strengths:
- ...
- ...

Weaknesses:
- ...
- ...

Missing Skills:
- ...

Suggestions:
- ...

Section Scores:
Education: <number>
Experience: <number>
Skills: <number>
Projects: <number>
```
Instead of forcing JSON, structured text was used to improve reliability. 

---

## ✅ What Worked Well
* Local LLM integration using Ollama worked smoothly
* Structured output + parsing made the system stable
* Retry + fallback mechanism handled model inconsistencies
* JD matching improved realism of results
* UI is clean and easy to understand

---

## ⚠️ Where AI Output Was Incorrect / Needed Fixes
* The model sometimes:
  * skipped fields
  * returned invalid JSON
  * gave generic or irrelevant weaknesses
  * misinterpreted job descriptions

Fixes applied:
* switched from JSON output → structured text parsing
* added retry mechanism
* added validation layer for missing fields
* improved JD matching using skill-based logic
* handled OR conditions (e.g., Flask/Django/Pyramid)

---

## ⚙️ Assumptions Made
* Resume is in English
* PDF contains readable text (not scanned images)
* Job description is optional but improves results
* Skill matching is based on keyword presence (not deep semantic understanding)
* Local LLM may not always be 100% accurate, so validation is required

---

## 🚀 Possible Improvements (with more time)
* Use embeddings for better JD matching (semantic similarity)
* Support DOC/DOCX files
* Improve UI with charts/visual analytics
* Add user authentication and history tracking
* Deploy as a web service

---

## 🤖 Use of AI During Development

### Where AI was used

AI was used mainly in the following parts of the project:

- Resume analysis (core feature)
- Generating structured feedback (score, summary, strengths, etc.)
- Initial prompt design
- Assisting in debugging and improving code structure during development

---

### How AI was used

A local LLM (via Ollama) was used to analyze resume content and generate feedback.

Instead of relying on direct JSON output (which was inconsistent), the model was guided to produce structured text, which was then parsed into a usable format.

AI tools were also used during development to:
- speed up initial coding
- explore different approaches for parsing and validation
- refine prompt design

---

### What was verified or fixed manually

Several issues required manual intervention:

- The model often returned invalid or incomplete JSON → replaced with structured text parsing
- Some outputs were too generic → added validation and post-processing logic
- Job description matching initially gave poor results → improved using skill-based matching
- Incorrect skill detection (e.g., treating Django/Flask as separate mandatory skills) → fixed using grouped skill logic

Overall, AI helped accelerate development, but the final system required manual corrections to ensure reliability and meaningful output.

---

## 🎯 Final Note
This project focuses on **practical AI usage**, not just calling an API. The main effort was in handling unreliable AI output and making the system stable and usable.
