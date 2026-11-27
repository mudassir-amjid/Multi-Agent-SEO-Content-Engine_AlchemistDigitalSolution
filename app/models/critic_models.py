from pydantic import BaseModel, Field


class CriticFeedback(BaseModel):

    seo_score: int = Field(ge=0, le=20)

    readability_score: int = Field(ge=0, le=20)

    factual_consistency_score: int = Field(ge=0, le=25)

    structure_score: int = Field(ge=0, le=15)

    originality_score: int = Field(ge=0, le=20)

    total_score: int = Field(ge=0, le=100)

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    improvement_suggestions: list[str] = Field(
        default_factory=list
    )

    revision_required: bool

    overall_feedback: str = ""