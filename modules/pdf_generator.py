import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet

OUTPUT_DIR = "outputs/reports"


def generate_pdf(data: dict, filename: str = "resume_report.pdf") -> str:
    """
    Generate PDF report from analysis data.
    Returns file path.
    """

    try:
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        file_path = os.path.join(OUTPUT_DIR, filename)

        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        content = []

        # Title
        content.append(Paragraph("AI Resume Analysis Report", styles["Title"]))
        content.append(Spacer(1, 12))

        # Score
        content.append(Paragraph(f"<b>Overall Score:</b> {data.get('score', 0)}/100", styles["Normal"]))
        content.append(Spacer(1, 12))

        # Summary
        content.append(Paragraph("<b>Summary:</b>", styles["Heading2"]))
        content.append(Paragraph(data.get("summary", ""), styles["Normal"]))
        content.append(Spacer(1, 12))

        # Strengths
        content.append(Paragraph("<b>Strengths:</b>", styles["Heading2"]))
        strengths = data.get("strengths", [])
        content.append(ListFlowable([Paragraph(s, styles["Normal"]) for s in strengths]))
        content.append(Spacer(1, 12))

        # Weaknesses
        content.append(Paragraph("<b>Weaknesses:</b>", styles["Heading2"]))
        weaknesses = data.get("weaknesses", [])
        content.append(ListFlowable([Paragraph(w, styles["Normal"]) for w in weaknesses]))
        content.append(Spacer(1, 12))

        # Missing Skills
        content.append(Paragraph("<b>Missing Skills:</b>", styles["Heading2"]))
        missing = data.get("missing_skills", [])
        content.append(ListFlowable([Paragraph(m, styles["Normal"]) for m in missing]))
        content.append(Spacer(1, 12))

        # Suggestions
        content.append(Paragraph("<b>Suggestions:</b>", styles["Heading2"]))
        suggestions = data.get("suggestions", [])
        content.append(ListFlowable([Paragraph(s, styles["Normal"]) for s in suggestions]))
        content.append(Spacer(1, 12))

        # Section Scores
        content.append(Paragraph("<b>Section Scores:</b>", styles["Heading2"]))
        section_scores = data.get("section_scores", {})
        for key, value in section_scores.items():
            content.append(Paragraph(f"{key.capitalize()}: {value}", styles["Normal"]))

        # Build PDF
        doc.build(content)

        return file_path

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return ""