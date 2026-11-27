import json

from app.agents.research_agent import ResearchAgent
from app.models.input_models import ArticleRequest


# Initialize Research Agent
agent = ResearchAgent()


# Create sample user input
request = ArticleRequest(
    topic="Artificial Intelligence in Healthcare",
    target_keyword="AI in Healthcare",
    audience="Beginners",
    tone="Professional"
)


# Mock Gemini response (no API call)
mock_response = {
    "topic": "Artificial Intelligence in Healthcare",
    "target_keyword": "AI in Healthcare",
    "search_intent": "Informational",
    "related_keywords": [
        "AI in medicine",
        "machine learning in healthcare",
        "AI medical diagnosis"
    ],
    "key_facts": [
        "AI can assist healthcare professionals in analyzing medical data.",
        "AI tools can support medical imaging analysis."
    ],
    "content_brief": (
        "Explain AI in healthcare, its applications, "
        "benefits, limitations, and future possibilities "
        "in beginner-friendly language."
    ),
    "audience": "Beginners",
    "reference_urls": []
}


# Replace Gemini call with mock response
agent.gemini.generate_response = lambda prompt: json.dumps(mock_response)


# Run Research Agent
result = agent.run(request)


# Verify results
assert result is not None
assert result.topic == "Artificial Intelligence in Healthcare"
assert result.search_intent == "Informational"
assert len(result.related_keywords) == 3


print("Research Agent Test: PASSED")
print("\nResearch Result:")
print(result.model_dump_json(indent=2))
