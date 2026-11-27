from pydantic import BaseModel, Field


class ArticleContent(BaseModel):

    title: str

    content_markdown: str = Field(
        min_length=100,
        description="Complete article in Markdown format"
    )

    word_count: int = Field(
        ge=0
    )

    bilingual_summary: str = Field(
        default="",
        description="Roman Urdu or bilingual article summary"
    )

    language: str = "English"