
from google import genai
from app.core.config import GEMINI_API_KEY

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Send a simple test request
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Reply with exactly: Gemini connection successful!"
)

print("\nGemini Response:")
print(response.text)
