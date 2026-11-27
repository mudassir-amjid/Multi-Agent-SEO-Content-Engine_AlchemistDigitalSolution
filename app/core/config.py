
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

print("Gemini API configuration loaded successfully!")
