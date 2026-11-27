
import json

from app.services.gemini_service import GeminiService
from app.models.research_models import ResearchResult
from app.models.outline_models import ArticleOutline
from app.models.article_models import ArticleContent


class WriterAgent:

    def __init__(self):
        self.name = "Long-form Editorial Writer"
        self.gemini = GeminiService()

    def build_prompt(self, research, outline, revision_feedback=None):

        revision_instruction = ""

        if revision_feedback:
            revision_instruction = f"""
IMPORTANT: This is a revision of an earlier article.

Critic feedback:
{revision_feedback}

Improve the article by addressing the feedback.
Keep the article consistent with the research and outline.
"""

        return f"""
You are an expert editorial writer and SEO content specialist.

RESEARCH:
{research.model_dump_json(indent=2)}

ARTICLE OUTLINE:
{outline.model_dump_json(indent=2)}

Write an original article of approximately 1000-1500 words.

Requirements:
- Follow the supplied outline.
- Use natural, professional language.
- Use the main and related keywords naturally.
- Avoid repetition and filler.
- Do not invent facts or statistics.
- Stay consistent with the supplied research.
- Include an FAQ section answering the supplied questions.
- Include an informative conclusion.
- Use Markdown headings.
- Provide an English and Roman Urdu summary.

{revision_instruction}

Return valid JSON only, without Markdown code fences.

Use this structure:
{{
    "title": "",
    "content_markdown": "",
    "word_count": 0,
    "bilingual_summary": "",
    "language": "English"
}}
"""

    def run(self, research, outline, revision_feedback=None):

        try:
            prompt = self.build_prompt(
                research,
                outline,
                revision_feedback
            )

            response = self.gemini.generate_response(prompt)

            if not response:
                raise ValueError("Gemini returned an empty response.")

            article_data = json.loads(response)

            return ArticleContent.model_validate(article_data)

        except Exception as e:
            print(f"Writer Agent failed: {e}")
            return None


if __name__ == "__main__":
    agent = WriterAgent()
    print("Writer Agent:", agent.name)
    print("Writer Agent initialized successfully!")
