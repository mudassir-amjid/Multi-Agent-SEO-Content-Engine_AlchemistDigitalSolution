
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.models.input_models import ArticleRequest
from app.services.pipeline_service import EditorialPipeline
from app.database.db import (
    initialize_database,
    save_article,
    list_articles,
    get_article,
    update_article_status
)


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

app = FastAPI(
    title="Multi-Agent Editorial & SEO Engine",
    description=(
        "AI-powered multi-agent system for SEO research, "
        "content outlining, article writing and quality review."
    ),
    version="1.0.0"
)

# Dashboard HTML file location
FRONTEND_FILE = (
    Path(__file__).resolve().parents[2]
    / "frontend"
    / "index.html"
)


# --------------------------------------------------
# DATABASE STARTUP
# --------------------------------------------------

@app.on_event("startup")
def startup():
    initialize_database()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.get("/", include_in_schema=False)
def dashboard():
    if not FRONTEND_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="Dashboard file not found. Check frontend/index.html"
        )

    return FileResponse(FRONTEND_FILE)


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "Multi-Agent Editorial & SEO Engine"
    }


# --------------------------------------------------
# GENERATE ARTICLE
# --------------------------------------------------

@app.post("/api/generate")
def generate_article(request: ArticleRequest):

    try:
        pipeline = EditorialPipeline()

        result = pipeline.run(request)

        if result["status"] != "completed":
            raise HTTPException(
                status_code=500,
                detail=result.get(
                    "error",
                    "Editorial pipeline execution failed"
                )
            )

        # Save generated article in database
        saved_article = save_article(result)

        return {
            "message": "Article generated and saved successfully",
            "article": saved_article,
            "pipeline_result": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# GET ALL ARTICLES
# --------------------------------------------------

@app.get("/api/articles")
def get_articles():

    try:
        return list_articles()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# GET SINGLE ARTICLE
# --------------------------------------------------

@app.get("/api/articles/{article_id}")
def get_article_by_id(article_id: str):

    article = get_article(article_id)

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    return article


# --------------------------------------------------
# UPDATE ARTICLE STATUS
# --------------------------------------------------

class StatusUpdate(BaseModel):
    status: str


@app.patch("/api/articles/{article_id}/status")
def change_article_status(
    article_id: str,
    update: StatusUpdate
):

    allowed_statuses = ["draft", "approved", "published"]

    if update.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Status must be draft, approved, or published"
        )

    article = update_article_status(
        article_id,
        update.status
    )

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    return {
        "message": "Article status updated successfully",
        "article": article
    }
