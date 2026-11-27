from pydantic import BaseModel, Field


class ArticleRequest(BaseModel):
    topic: str = Field(
        min_length=3,
        description="Topic of the article"
    )

    target_keyword: str = Field(
        min_length=2,
        description="Main SEO keyword"
    )

    audience: str = Field(
        default="General audience",
        description="Target readers"
    )

    tone: str = Field(
        default="Professional",
        description="Writing tone"
    )

    language: str = Field(
        default="English",
        description="Article language"
    )

    reference_urls: list[str] = Field(
        default_factory=list,
        description="Optional reference URLs"
    )