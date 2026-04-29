import os
from dotenv import load_dotenv

# Force .env to override any system variables
load_dotenv(override=True)

# --- MODEL CONFIG (Ollama) ---
OLLAMA_MODEL = "llama3.2:latest"

# --- INPUT LIMITS ---
# Keep it small to avoid JSON breaking in local LLM
MAX_INPUT_CHARS = 2500

# --- FILE PATHS ---
SKILLS_FILE = "assets/skills.txt"
OUTPUT_DIR = "outputs/reports"

# --- DEFAULTS ---
DEFAULT_SCORE = 70

# --- OPTIONAL: API KEYS (if you ever switch back) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")