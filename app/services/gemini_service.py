from google import genai
from app.core.config import GEMINI_API_KEY


class GeminiService:

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model_name = "gemini-3.8-flash"

    def generate_response(self, prompt: str):

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        return response.text


if __name__ == "__main__":
    service = GeminiService()

    print("Gemini Service initialized successfully!")
    print("Model:", service.model_name)
    