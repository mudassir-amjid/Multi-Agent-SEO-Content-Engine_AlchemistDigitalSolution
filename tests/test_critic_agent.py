
import json

from app.agents.critic_agent import CriticAgent
from app.models.research_models import ResearchResult
from app.models.outline_models import ArticleOutline
from app.models.article_models import ArticleContent


agent = CriticAgent()

research = ResearchResult(
    topic="Artificial Intelligence in Healthcare",
    target_keyword="AI in Healthcare",
    search_intent="Informational",
    related_keywords=["AI in medicine", "machine learning in healthcare"],
    key_facts=[
        "AI can assist healthcare professionals in analyzing medical data.",
        "AI tools can support medical imaging analysis."
    ],
    content_brief="Explain AI applications, benefits and limitations.",
    audience="Beginners",
    reference_urls=[]
)

outline = ArticleOutline(
    h1="How AI Is Transforming Healthcare",
    sections=[
        {"h2": "Introduction to AI", "h3": ["What is AI?"]},
        {"h2": "Applications of AI", "h3": ["Medical Imaging"]},
    ],
    faq=["What is AI in healthcare?"],
    meta_title="AI in Healthcare: Uses and Benefits",
    meta_description="Explore AI applications, benefits and limitations in healthcare."
)

article = ArticleContent(
    title="How AI Is Transforming Healthcare",
    content_markdown=(
        "# How AI Is Transforming Healthcare\n\n"
        "## Introduction to AI\n\n"
        "Artificial intelligence can assist healthcare professionals "
        "in analyzing medical data. It can also support medical imaging "
        "analysis. These applications may help professionals in their work.\n\n"
        "## Applications of AI\n\n"
        "AI tools can support the analysis of medical images. They can "
        "also help organize and analyze patient information.\n\n"
        "## Conclusion\n\n"
        "AI has useful applications in healthcare, but its limitations "
        "and responsible use must also be considered."
    ),
    word_count=75,
    bilingual_summary="English: AI supports healthcare. Roman Urdu: AI healthcare mein madad deti hai.",
    language="English"
)

# Mock Critic response: scores add up to 85
mock_response = {
    "seo_score": 17,
    "readability_score": 18,
    "factual_consistency_score": 22,
    "structure_score": 13,
    "originality_score": 15,
    "total_score": 85,
    "strengths": [
        "Clear headings",
        "Relevant keyword usage"
    ],
    "weaknesses": [
        "Article needs more depth"
    ],
    "improvement_suggestions": [
        "Add more useful examples"
    ],
    "revision_required": False,
    "overall_feedback": "Good structure and readability, but expand the article."
}

# Mock Gemini response
agent.gemini.generate_response = lambda prompt: json.dumps(mock_response)

# Run Critic Agent
result = agent.run(research, outline, article)

# Verify results
assert result is not None
assert result.total_score == 85
assert result.revision_required is False
assert (
    result.seo_score
    + result.readability_score
    + result.factual_consistency_score
    + result.structure_score
    + result.originality_score
) == 85

print("Critic Agent Test: PASSED")
print("\nCritic Feedback:")
print(result.model_dump_json(indent=2))
