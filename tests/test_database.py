
from app.database.db import (
    initialize_database,
    save_article,
    list_articles,
    get_article,
    update_article_status
)

# Sample pipeline result — no Gemini API call required
sample_result = {
    "research": {
        "topic": "Artificial Intelligence in Healthcare",
        "target_keyword": "AI in Healthcare",
        "search_intent": "Informational"
    },
    "outline": {
        "h1": "How AI Is Transforming Healthcare",
        "meta_title": "AI in Healthcare: Uses and Benefits",
        "meta_description": "Explore AI applications and benefits in healthcare.",
        "sections": [],
        "faq": []
    },
    "article": {
        "title": "How AI Is Transforming Healthcare",
        "content_markdown": "# How AI Is Transforming Healthcare\n\nAI can support healthcare professionals.",
        "bilingual_summary": "AI healthcare mein madad karti hai."
    },
    "critic_feedback": {
        "total_score": 85
    }
}

print("\nStarting Database Test...")

initialize_database()

saved = save_article(sample_result)

assert saved is not None
assert saved["topic"] == "Artificial Intelligence in Healthcare"
assert saved["quality_score"] == 85
assert saved["status"] == "approved"

article_id = saved["id"]

retrieved = get_article(article_id)
assert retrieved is not None
assert retrieved["id"] == article_id

updated = update_article_status(article_id, "published")
assert updated["status"] == "published"

articles = list_articles()
assert any(article["id"] == article_id for article in articles)

print("\n===================================")
print("DATABASE TEST: PASSED")
print("===================================")
print("Article saved successfully.")
print("Article retrieved successfully.")
print("Article status updated successfully.")
print("Total articles in database:", len(articles))
print("Article ID:", article_id)

