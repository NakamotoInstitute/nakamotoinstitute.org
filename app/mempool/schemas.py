import datetime
from typing import List, Optional

from pydantic import AliasPath, BaseModel, Field, field_serializer
from pydantic.alias_generators import to_camel

from ..authors.schemas import AuthorSchema
from ..translators.schemas import TranslatorSchema


class MempoolCanonicalMDSchema(BaseModel):
    authors: List[str]
    image: Optional[str] = None
    date: datetime.date
    added: Optional[datetime.date] = None
    original_url: Optional[str] = None
    original_site: Optional[str] = None


class MempoolMDSchema(BaseModel):
    title: str
    excerpt: str
    image_alt: Optional[str] = None


class MempoolTranslatedMDSchema(MempoolMDSchema):
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    translation_url: Optional[str] = None
    translation_site: Optional[str] = None
    translation_site_url: Optional[str] = None
    translators: Optional[List[str]] = []


class MempoolTranslationSchema(BaseModel):
    language: str
    title: str
    slug: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class MempoolPostBaseSchema(BaseModel):
    language: str
    title: str
    slug: str
    excerpt: str
    image_alt: Optional[str]
    translation_url: Optional[str]
    translation_site: Optional[str]
    translation_site_url: Optional[str]
    date: datetime.date = Field(alias=AliasPath("blog_post", "date"))
    added: datetime.date = Field(alias=AliasPath("blog_post", "added"))
    authors: List[AuthorSchema] = Field(alias=AliasPath("blog_post", "authors"))
    translations: List[MempoolTranslationSchema]
    translators: List[TranslatorSchema]

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


class MempoolPostSchema(MempoolPostBaseSchema):
    content: str
