
import sqlite3
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parents[2] / "articles.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id TEXT PRIMARY KEY,
                topic TEXT NOT NULL,
                target_keyword TEXT NOT NULL,
                search_intent TEXT,
                meta_title TEXT,
                meta_description TEXT,
                outline_json TEXT,
                content_markdown TEXT,
                bilingual_summary TEXT,
                quality_score INTEGER,
                status TEXT DEFAULT 'draft',
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_runs (
                id TEXT PRIMARY KEY,
                article_id TEXT,
                agent_name TEXT NOT NULL,
                input_tokens INTEGER DEFAULT 0,
                output_tokens INTEGER DEFAULT 0,
                latency_ms INTEGER DEFAULT 0,
                critic_feedback_json TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(article_id) REFERENCES articles(id)
            )
        """)


def save_article(result):
    article_id = str(uuid.uuid4())

    research = result["research"]
    outline = result["outline"]
    article = result["article"]
    feedback = result["critic_feedback"]

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO articles (
                id, topic, target_keyword, search_intent,
                meta_title, meta_description, outline_json,
                content_markdown, bilingual_summary,
                quality_score, status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            article_id,
            research["topic"],
            research["target_keyword"],
            research["search_intent"],
            outline["meta_title"],
            outline["meta_description"],
            json.dumps(outline),
            article["content_markdown"],
            article["bilingual_summary"],
            feedback["total_score"],
            "approved" if feedback["total_score"] >= 80 else "draft",
            datetime.now(timezone.utc).isoformat()
        ))

    return get_article(article_id)


def list_articles():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM articles ORDER BY created_at DESC"
        ).fetchall()

    return [dict(row) for row in rows]


def get_article(article_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM articles WHERE id = ?",
            (article_id,)
        ).fetchone()

    return dict(row) if row else None


def update_article_status(article_id, status):
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE articles SET status = ? WHERE id = ?",
            (status, article_id)
        )

    if cursor.rowcount == 0:
        return None

    return get_article(article_id)
