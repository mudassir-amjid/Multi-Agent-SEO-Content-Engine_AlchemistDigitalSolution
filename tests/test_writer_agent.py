
import json

from app.agents.writer_agent import WriterAgent
from app.models.research_models import ResearchResult
from app.models.outline_models import ArticleOutline


agent = WriterAgent()

# Sample research
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

# Sample outline
outline = ArticleOutline(
    h1="How Artificial Intelligence Is Transforming Healthcare",
    sections=[
        {
            "h2": "What Is AI in Healthcare?",
            "h3": ["Understanding Artificial Intelligence"]
        },
        {
            "h2": "Applications of AI in Healthcare",
            "h3": ["Medical Imaging", "Patient Data Analysis"]
        },
        {
            "h2": "Benefits and Limitations",
            "h3": ["Benefits", "Challenges"]
        }
    ],
    faq=["What is AI in healthcare?", "Can AI replace doctors?"],
    meta_title="AI in Healthcare: Uses and Benefits",
    meta_description="Discover how AI is changing healthcare and medical services."
)

# Mock article response
mock_response = {
    "title": "How Artificial Intelligence Is Transforming Healthcare",
    "content_markdown": (
        "# How Artificial Intelligence Is Transforming Healthcare\n\n"
        "## What Is AI in Healthcare?\n\n"
        "Artificial intelligence refers to computer systems that "
        "perform tasks that normally require human intelligence. "
        "In healthcare, these tools can help professionals analyze "
        "medical data and support decision-making.\n\n"
        "## Applications of AI in Healthcare\n\n"
        "AI tools can support medical imaging analysis and patient "
        "data analysis. These applications can assist healthcare "
        "professionals in their work.\n\n"
        "## Benefits and Limitations\n\n"
        "AI offers useful support, but it also has limitations. "
        "Healthcare professionals must consider accuracy, privacy "
        "and responsible use.\n\n"
        "## Conclusion\n\n"
        "AI is an important developing technology in healthcare."
    ),
    "word_count": 100,
    "bilingual_summary": (
        "English: AI helps healthcare professionals analyze data.\n"
        "Roman Urdu: AI doctors ko medical data samajhne mein madad "
        "de sakti hai."
    ),
    "language": "English"
}

# Mock Gemini response
agent.gemini.generate_response = lambda prompt: json.dumps(mock_response)

# Run Writer Agent
result = agent.run(research, outline)

# Verify
assert result is not None
assert result.title.startswith("How Artificial Intelligence")
assert result.word_count == 100
assert "Roman Urdu" in result.bilingual_summary
assert len(result.content_markdown) >= 100

print("Writer Agent Test: PASSED")
print("\nGenerated Article:")
print(result.model_dump_json(indent=2))

