from pydantic import BaseModel, Field


class OutlineSection(BaseModel):
    h2: str

    h3: list[str] = Field(
        default_factory=list
    )


class ArticleOutline(BaseModel):
    h1: str

    sections: list[OutlineSection] = Field(
        default_factory=list
    )

    faq: list[str] = Field(
        default_factory=list
    )

    meta_title: str = Field(
        max_length=60
    )

    meta_description: str = Field(
        max_length=155
    )