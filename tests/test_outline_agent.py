
import json

from app.agents.outline_agent import OutlineAgent
from app.models.research_models import ResearchResult


agent = OutlineAgent()

# Sample research data from Agent 1
research = ResearchResult(
    topic="Artificial Intelligence in Healthcare",
    target_keyword="AI in Healthcare",
    search_intent="Informational",
    related_keywords=[
        "AI in medicine",
        "machine learning in healthcare",
        "AI medical diagnosis"
    ],
    key_facts=[
        "AI can assist healthcare professionals in analyzing medical data.",
        "AI tools can support medical imaging analysis."
    ],
    content_brief=(
        "Explain AI in healthcare, its applications, benefits, "
        "limitations, and future possibilities."
    ),
    audience="Beginners",
    reference_urls=[]
)

# Mock Gemini response
mock_response = {
    "h1": "How Artificial Intelligence Is Transforming Healthcare",
    "sections": [
        {
            "h2": "What Is AI in Healthcare?",
            "h3": [
                "Understanding Artificial Intelligence",
                "How AI Works in Medicine"
            ]
        },
        {
            "h2": "Applications of AI in Healthcare",
            "h3": [
                "Medical Imaging",
                "Patient Data Analysis"
            ]
        },
        {
            "h2": "Benefits and Limitations of AI",
            "h3": [
                "Benefits for Healthcare Professionals",
                "Challenges and Risks"
            ]
        }
    ],
    "faq": [
        "What is AI in healthcare?",
        "How is AI used in medical diagnosis?",
        "Can AI replace doctors?",
        "What are the limitations of AI in healthcare?"
    ],
    "meta_title": "AI in Healthcare: Uses, Benefits and Challenges",
    "meta_description": (
        "Explore how AI is transforming healthcare, "
        "including its applications, benefits, and limitations."
    )
}

# Replace real Gemini call with mock response
agent.gemini.generate_response = lambda prompt: json.dumps(mock_response)

# Run Agent 2
result = agent.run(research)

# Verify output
assert result is not None
assert result.h1.startswith("How Artificial Intelligence")
assert len(result.sections) == 3
assert len(result.faq) == 4
assert len(result.meta_title) <= 60
assert len(result.meta_description) <= 155

print("Outline Agent Test: PASSED")
print("\nGenerated Outline:")
print(result.model_dump_json(indent=2))
