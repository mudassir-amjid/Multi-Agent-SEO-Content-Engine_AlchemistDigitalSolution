
import json

from app.services.gemini_service import GeminiService
from app.models.research_models import ResearchResult
from app.models.outline_models import ArticleOutline
from app.models.article_models import ArticleContent
from app.models.critic_models import CriticFeedback


class CriticAgent:

    def __init__(self):
        self.name = "Editorial Quality & SEO Critic"
        self.gemini = GeminiService()

    def build_prompt(
        self,
        research: ResearchResult,
        outline: ArticleOutline,
        article: ArticleContent
    ):

        return f"""
You are a professional SEO editor and content quality evaluator.

Evaluate the article using the supplied research and outline.

RESEARCH:
{research.model_dump_json(indent=2)}

OUTLINE:
{outline.model_dump_json(indent=2)}

ARTICLE:
{article.model_dump_json(indent=2)}

Evaluate these five areas:

1. SEO Score: 0-20
   - Main keyword usage
   - Related keyword usage
   - SEO relevance

2. Readability Score: 0-20
   - Clear language
   - Readability
   - Natural writing

3. Factual Consistency Score: 0-25
   - Consistency with research
   - Unsupported claims
   - Factual accuracy based on supplied material

4. Structure Score: 0-15
   - Headings
   - Organization
   - Flow

5. Originality Score: 0-20
   - Original expression
   - Repetition
   - Unnecessary filler

Calculate total_score as the sum of all five scores.

Rules:
- Total score must be between 0 and 100.
- If total_score is below 80, revision_required must be true.
- If total_score is 80 or above, revision_required must be false.
- Give useful strengths, weaknesses and suggestions.
- Do not claim external fact-checking was performed.

Return valid JSON only. No Markdown code fences.

Use this exact structure:

{{
    "seo_score": 0,
    "readability_score": 0,
    "factual_consistency_score": 0,
    "structure_score": 0,
    "originality_score": 0,
    "total_score": 0,
    "strengths": [],
    "weaknesses": [],
    "improvement_suggestions": [],
    "revision_required": true,
    "overall_feedback": ""
}}
"""

    def run(
        self,
        research: ResearchResult,
        outline: ArticleOutline,
        article: ArticleContent
    ):

        try:
            prompt = self.build_prompt(research, outline, article)

            response = self.gemini.generate_response(prompt)

            if not response:
                raise ValueError("Gemini returned an empty response.")

            feedback_data = json.loads(response)

            result = CriticFeedback.model_validate(feedback_data)

            # Verify total score
            calculated_score = (
                result.seo_score
                + result.readability_score
                + result.factual_consistency_score
                + result.structure_score
                + result.originality_score
            )

            if result.total_score != calculated_score:
                raise ValueError("Critic total score calculation is incorrect.")

            if result.revision_required != (result.total_score < 80):
                raise ValueError("Revision decision does not match score.")

            return result

        except Exception as e:
            print(f"Critic Agent failed: {e}")
            return None


if __name__ == "__main__":
    agent = CriticAgent()
    print("Critic Agent:", agent.name)
    print("Critic Agent initialized successfully!")
