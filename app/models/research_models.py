from pydantic import BaseModel, Field


class ResearchResult(BaseModel):

    topic: str

    target_keyword: str

    search_intent: str = Field(
        description="Informational, Commercial, or News Analysis"
    )

    related_keywords: list[str] = Field(
        default_factory=list
    )

    key_facts: list[str] = Field(
        default_factory=list
    )

    content_brief: str = ""

    audience: str = "General audience"

    reference_urls: list[str] = Field(
        default_factory=list
    )