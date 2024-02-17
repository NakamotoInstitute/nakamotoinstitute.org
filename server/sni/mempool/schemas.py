import datetime
from typing import Any

from pydantic import AliasPath, BaseModel, Field, field_serializer, model_validator

from sni.authors.schemas.base import AuthorModel
from sni.constants import Locales
from sni.shared.schemas import ORMModel, TranslationSchema
from sni.translators.schemas import TranslatorModel


class MempoolCanonicalMDModel(BaseModel):
    authors: list[str]
    image: str | None = None
    date: datetime.date
    added: datetime.date
    original_url: str | None = None
    original_site: str | None = None
    series: str | None = None
    series_index: int | None = None
    has_math: bool | None = False

    @model_validator(mode="before")
    @classmethod
    def check_added(cls, data: Any) -> Any:
        if data.get("added", None) is None:
            data["added"] = data["date"]
        return data


class BaseMempoolMDModel(BaseModel):
    title: str
    image_alt: str | None = None


class MempoolMDModel(BaseMempoolMDModel):
    excerpt: str


class MempoolTranslationMDModel(BaseMempoolMDModel):
    slug: str | None = None
    excerpt: str | None = None
    translation_url: str | None = None
    translation_site: str | None = None
    translation_site_url: str | None = None
    translators: list[str] = []


class MempoolSeriesCanonicalMDModel(BaseModel):
    chapter_title: bool | None = False


class MempoolSeriesMDModel(BaseModel):
    title: str


class MempoolSeriesTranslationMDModel(MempoolSeriesMDModel):
    slug: str | None = None


class MempoolSeriesBaseModel(ORMModel):
    locale: Locales
    title: str
    slug: str
    chapter_title: bool | None = Field(
        validation_alias=AliasPath("blog_series", "chapter_title"),
        serialization_alias="chapterTitle",
    )


class MempoolPostBaseModel(ORMModel):
    locale: Locales
    title: str
    slug: str
    excerpt: str
    image: str | None = Field(validation_alias=AliasPath("blog_post", "image"))
    image_alt: str | None
    original_url: str | None = Field(
        validation_alias=AliasPath("blog_post", "original_url"),
        serialization_alias="originalUrl",
    )
    original_site: str | None = Field(
        validation_alias=AliasPath("blog_post", "original_site"),
        serialization_alias="originalSite",
    )
    translation_url: str | None
    translation_site: str | None
    translation_site_url: str | None
    date: datetime.date = Field(validation_alias=AliasPath("blog_post", "date"))
    added: datetime.date = Field(validation_alias=AliasPath("blog_post", "added"))
    authors: list[AuthorModel] = Field(
        validation_alias=AliasPath("blog_post", "authors")
    )
    translations: list[TranslationSchema]
    series_index: int | None = Field(
        validation_alias=AliasPath("blog_post", "series_index"),
        serialization_alias="seriesIndex",
    )
    series: MempoolSeriesBaseModel | None = None

    @field_serializer("date")
    def serialize_date(self, date: datetime.date) -> str:
        return date.isoformat()

    @field_serializer("added")
    def serialize_added(self, added: datetime.date) -> str:
        return added.isoformat()


class MempoolPostIndexModel(MempoolPostBaseModel):
    has_content: bool = False

    @model_validator(mode="before")
    @classmethod
    def check_content(cls, data: Any) -> Any:
        data.has_content = bool(data.html_content)
        return data


class MempoolPostModel(MempoolPostBaseModel):
    html_content: str = Field(alias="content")
    has_math: bool = Field(
        validation_alias=AliasPath("blog_post", "has_math"),
        serialization_alias="hasMath",
    )
    translators: list[TranslatorModel]


class MempoolSeriesModel(MempoolSeriesBaseModel):
    translations: list[MempoolSeriesBaseModel]


class MempoolSeriesFullModel(BaseModel):
    series: MempoolSeriesModel
    posts: list[MempoolPostIndexModel]
