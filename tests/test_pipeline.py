
import json

from app.services.pipeline_service import EditorialPipeline
from app.models.input_models import ArticleRequest
from app.models.research_models import ResearchResult
from app.models.outline_models import ArticleOutline
from app.models.article_models import ArticleContent
from app.models.critic_models import CriticFeedback


# Initialize pipeline
pipeline = EditorialPipeline()


# Sample user request
request = ArticleRequest(
    topic="Artificial Intelligence in Healthcare",
    target_keyword="AI in Healthcare",
    audience="Beginners",
    tone="Professional",
    language="English"
)


# Mock Research Agent
def mock_research(request):

    return ResearchResult(
        topic=request.topic,
        target_keyword=request.target_keyword,
        search_intent="Informational",
        related_keywords=[
            "AI in medicine",
            "machine learning in healthcare"
        ],
        key_facts=[
            "AI can assist healthcare professionals in analyzing medical data.",
            "AI tools can support medical imaging analysis."
        ],
        content_brief="Explain AI applications, benefits and limitations.",
        audience=request.audience,
        reference_urls=[]
    )


# Mock SEO Outliner Agent
def mock_outline(research):

    return ArticleOutline(
        h1="How AI Is Transforming Healthcare",
        sections=[
            {
                "h2": "Introduction to AI",
                "h3": ["What is AI?"]
            },
            {
                "h2": "Applications of AI",
                "h3": ["Medical Imaging"]
            }
        ],
        faq=[
            "What is AI in healthcare?"
        ],
        meta_title="AI in Healthcare: Uses and Benefits",
        meta_description="Explore AI applications and benefits in healthcare."
    )


# Mock Editorial Writer Agent
def mock_writer(research, outline, revision_feedback=None):

    return ArticleContent(
        title="How AI Is Transforming Healthcare",
        content_markdown=(
            "# How AI Is Transforming Healthcare\n\n"
            "## Introduction to AI\n\n"
            "Artificial intelligence can assist healthcare professionals "
            "in analyzing medical data and supporting medical imaging analysis.\n\n"
            "## Applications of AI\n\n"
            "AI tools can support the analysis of medical images. "
            "They can also help organize and analyze patient information.\n\n"
            "## Conclusion\n\n"
            "AI has useful applications in healthcare, but its limitations "
            "and responsible use must also be considered."
        ),
        word_count=100,
        bilingual_summary=(
            "English: AI supports healthcare. "
            "Roman Urdu: AI healthcare mein madad karti hai."
        ),
        language="English"
    )


# Mock Editorial Critic Agent
def mock_critic(research, outline, article):

    return CriticFeedback(
        seo_score=17,
        readability_score=18,
        factual_consistency_score=22,
        structure_score=13,
        originality_score=15,
        total_score=85,
        strengths=[
            "Clear structure",
            "Relevant keywords"
        ],
        weaknesses=[
            "Article needs more detail"
        ],
        improvement_suggestions=[
            "Add more examples"
        ],
        revision_required=False,
        overall_feedback="Good initial quality."
    )


# Connect mock agents to pipeline
pipeline.research_agent.run = mock_research
pipeline.outline_agent.run = mock_outline
pipeline.writer_agent.run = mock_writer
pipeline.critic_agent.run = mock_critic


# Execute complete pipeline
print("\nStarting Complete Editorial Pipeline Test...\n")

result = pipeline.run(request)


# Verify pipeline results
assert result["status"] == "completed"
assert result["quality_score"] == 85
assert result["approved"] is True

assert result["research"]["topic"] == request.topic
assert result["outline"]["h1"] == "How AI Is Transforming Healthcare"
assert result["article"]["title"] == "How AI Is Transforming Healthcare"
assert result["critic_feedback"]["total_score"] == 85


# Display final result
print("\n" + "=" * 45)
print("COMPLETE PIPELINE TEST: PASSED")
print("=" * 45)

print("Quality Score:", result["quality_score"])
print("Approved:", result["approved"])

print("\nPipeline Output:")
print(json.dumps(result, indent=2))

print("\nAll four agents connected successfully!")
