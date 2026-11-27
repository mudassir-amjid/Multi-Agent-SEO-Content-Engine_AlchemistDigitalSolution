
import json

from app.services.gemini_service import GeminiService
from app.models.research_models import ResearchResult
from app.models.outline_models import ArticleOutline


class OutlineAgent:

    def __init__(self):
        self.name = "SEO & Narrative Outliner"
        self.gemini = GeminiService()

    def build_prompt(self, research: ResearchResult):

        return f"""
You are an expert SEO strategist and editorial planner.

Create a detailed SEO article outline using the research below.

RESEARCH:
{research.model_dump_json(indent=2)}

REQUIREMENTS:

1. Create one clear H1 heading.
2. Create logical H2 sections.
3. Add relevant H3 subsections under H2 sections.
4. Create an SEO title with maximum 60 characters.
5. Create a meta description with maximum 155 characters.
6. Include 4 to 6 useful FAQs.
7. Follow the identified search intent.
8. Consider the target audience.
9. Do not introduce unsupported factual claims.
10. Avoid repetitive headings.

Return valid JSON only.
Do not use Markdown code fences.

Use this exact JSON structure:

{{
    "h1": "",
    "sections": [
        {{
            "h2": "",
            "h3": []
        }}
    ],
    "faq": [],
    "meta_title": "",
    "meta_description": ""
}}
"""

    def run(self, research: ResearchResult):

        try:
            prompt = self.build_prompt(research)

            response = self.gemini.generate_response(prompt)

            if not response:
                raise ValueError("Gemini returned an empty response.")

            outline_data = json.loads(response)

            result = ArticleOutline.model_validate(outline_data)

            if len(result.meta_title) > 60:
                raise ValueError("SEO title exceeds 60 characters.")

            if len(result.meta_description) > 155:
                raise ValueError("Meta description exceeds 155 characters.")

            return result

        except json.JSONDecodeError:
            print("Error: Gemini returned invalid JSON.")
            return None

        except Exception as e:
            print(f"Outline Agent failed: {e}")
            return None


if __name__ == "__main__":

    print("Outline Agent:", OutlineAgent().name)
    print("Outline Agent initialized successfully!")
