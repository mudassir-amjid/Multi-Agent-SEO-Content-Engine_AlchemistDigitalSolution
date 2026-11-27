
import json

from app.services.gemini_service import GeminiService
from app.models.input_models import ArticleRequest
from app.models.research_models import ResearchResult


class ResearchAgent:

    def __init__(self):
        self.name = "Research Agent"
        self.gemini = GeminiService()

    def build_prompt(self, request: ArticleRequest):

        return f"""
You are an expert SEO topic researcher.

Topic: {request.topic}
Target Keyword: {request.target_keyword}
Audience: {request.audience}
Tone: {request.tone}
Language: {request.language}
Reference URLs: {request.reference_urls}

Tasks:
1. Identify search intent.
2. Find relevant secondary keywords.
3. Identify important factual angles.
4. Prepare a useful content brief.
5. Consider the target audience.

Search intent must be:
Informational, Commercial, or News Analysis.

Rules:
- Do not invent statistics or factual claims.
- Do not claim live SERP research was performed.
- Distinguish verified facts from suggestions.
- Return valid JSON only.
- Do not use Markdown code fences.

Return this JSON structure:
{{
    "topic": "",
    "target_keyword": "",
    "search_intent": "Informational",
    "related_keywords": [],
    "key_facts": [],
    "content_brief": "",
    "audience": "",
    "reference_urls": []
}}
"""

    def run(self, request: ArticleRequest):

        try:
            prompt = self.build_prompt(request)

            response = self.gemini.generate_response(prompt)

            if not response:
                raise ValueError("Gemini returned an empty response.")

            research_data = json.loads(response)

            result = ResearchResult.model_validate(research_data)

            return result

        except json.JSONDecodeError:
            print("Error: Gemini returned invalid JSON.")
            return None

        except Exception as e:
            print(f"Research Agent failed: {e}")
            return None


if __name__ == "__main__":

    agent = ResearchAgent()

    request = ArticleRequest(
        topic="Artificial Intelligence in Healthcare",
        target_keyword="AI in Healthcare",
        audience="Beginners",
        tone="Professional"
    )

    prompt = agent.build_prompt(request)

    print("Research Agent:", agent.name)
    print("Error handling configured successfully.")
    print("Prompt generated successfully.")

