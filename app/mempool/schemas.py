import datetime
from typing import List, Optional

from pydantic import AliasPath, BaseModel, Field, field_serializer
from pydantic.alias_generators import to_camel

from ..authors.schemas import AuthorModel
from ..shared.schemas import TranslationSchema
from ..translators.schemas import TranslatorModel


class MempoolCanonicalMDModel(BaseModel):
    authors: List[str]
    image: Optional[str] = None
    date: datetime.date
    added: Optional[datetime.date] = None
    original_url: Optional[str] = None
    original_site: Optional[str] = None
    series: Optional[str] = None
    series_index: Optional[int] = None


class MempoolMDModel(BaseModel):
    title: str
    excerpt: str
    image_alt: Optional[str] = None


class MempoolTranslationMDModel(MempoolMDModel):
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    translation_url: Optional[str] = None
    translation_site: Optional[str] = None
    translation_site_url: Optional[str] = None
    translators: Optional[List[str]] = []


class MempoolSeriesCanonicalMDModel(BaseModel):
    chapter_title: Optional[bool] = False


class MempoolSeriesMDModel(BaseModel):
    title: str


class MempoolSeriesTranslationMDModel(MempoolSeriesMDModel):
    slug: Optional[str] = None


class MempoolSeriesBaseModel(BaseModel):
    locale: str
    title: str
    slug: str
    chapter_title: Optional[bool] = Field(
        validation_alias=AliasPath("blog_series", "chapter_title"),
        serialization_alias="chapterTitle",
    )

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class MempoolPostBaseModel(BaseModel):
    locale: str
    title: str
    slug: str
    excerpt: str
    image: Optional[str] = Field(alias=AliasPath("blog_post", "image"))
    image_alt: Optional[str]
    original_url: Optional[str] = Field(
        validation_alias=AliasPath("blog_post", "original_url"),
        serialization_alias="originalUrl",
    )
    original_site: Optional[str] = Field(
        validation_alias=AliasPath("blog_post", "original_site"),
        serialization_alias="originalSite",
    )
    translation_url: Optional[str]
    translation_site: Optional[str]
    translation_site_url: Optional[str]
    date: datetime.date = Field(alias=AliasPath("blog_post", "date"))
    added: datetime.date = Field(alias=AliasPath("blog_post", "added"))
    authors: List[AuthorModel] = Field(alias=AliasPath("blog_post", "authors"))
    translations: List[TranslationSchema]
    translators: List[TranslatorModel]
    series_index: Optional[int] = Field(
        validation_alias=AliasPath("blog_post", "series_index"),
        serialization_alias="seriesIndex",
    )
    series: Optional[MempoolSeriesBaseModel] = None

    @field_serializer("date")
    def serialize_date(self, date: datetime.date) -> str:
        return date.isoformat()

    @field_serializer("added")
    def serialize_added(self, added: datetime.date) -> str:
        return added.isoformat()

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class MempoolPostModel(MempoolPostBaseModel):
    content: str


class MempoolSeriesModel(MempoolSeriesBaseModel):
    translations: List[MempoolSeriesBaseModel]


class MempoolSeriesFullModel(BaseModel):
    series: MempoolSeriesModel
    posts: List[MempoolPostModel]
