from app.models.input_models import ArticleRequest
from app.models.research_models import ResearchResult
from app.models.outline_models import ArticleOutline
from app.models.article_models import ArticleContent
from app.models.critic_models import CriticFeedback


# Test 1: User Input Model
request = ArticleRequest(
    topic="Artificial Intelligence in Healthcare",
    target_keyword="AI in Healthcare"
)

print("1. User Input Model: PASSED")


# Test 2: Research Model
research = ResearchResult(
    topic=request.topic,
    target_keyword=request.target_keyword,
    search_intent="Informational"
)

print("2. Research Model: PASSED")


# Test 3: SEO Outline Model
outline = ArticleOutline(
    h1="AI in Healthcare",
    meta_title="AI in Healthcare: Uses and Benefits",
    meta_description="Explore how AI is transforming healthcare."
)

print("3. SEO Outline Model: PASSED")


# Test 4: Article Content Model
article = ArticleContent(
    title="AI in Healthcare",
    content_markdown="# AI in Healthcare\n\n" + ("This is a sample article. " * 10),
    word_count=50
)

print("4. Article Content Model: PASSED")


# Test 5: Critic Model
critic = CriticFeedback(
    seo_score=18,
    readability_score=18,
    factual_consistency_score=23,
    structure_score=14,
    originality_score=18,
    total_score=91,
    revision_required=False
)

print("5. Critic Model: PASSED")


print("\nAll 5 model tests completed successfully!")