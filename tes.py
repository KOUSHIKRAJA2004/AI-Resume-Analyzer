import os
from dotenv import load_dotenv

load_dotenv(override=True)

print(os.getenv("GEMINI_API_KEY"))