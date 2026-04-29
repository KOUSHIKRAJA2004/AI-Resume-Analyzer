import pdfplumber


def extract_text(file) -> str:
    """
    Extract text from uploaded PDF file.
    """
    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text.strip()

    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""