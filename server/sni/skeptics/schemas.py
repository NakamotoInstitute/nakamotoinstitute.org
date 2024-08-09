import datetime

from pydantic import BaseModel, field_serializer

from sni.shared.schemas import IteratableRootModel, ORMModel


class SkepticJSONModel(BaseModel):
    name: str
    name_slug: str
    title: str
    article: str | None = None
    date: datetime.date
    source: str
    excerpt: str | None = None
    link: str
    media_embed: str | None = None
    twitter_screenshot: bool = False
    wayback_link: str | None = None


class SkepticsJSONModel(IteratableRootModel):
    root: list[SkepticJSONModel]


class SkepticModel(ORMModel):
    name: str
    slug: str
    title: str
    article: str | None = None
    date: datetime.date
    source: str
    excerpt: str | None = None
    link: str
    media_embed: str | None = None
    twitter_screenshot: bool = False
    wayback_link: str | None = None

    @field_serializer("date")
    def serialize_date(self, date: datetime.date) -> str:
        return date.isoformat()

    @field_serializer("link")
    def serialize_link(self, link) -> list[str]:
        return [_link.strip() for _link in link.split(",")]
