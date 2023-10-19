import datetime
from typing import List, Optional

from pydantic import BaseModel, field_serializer

from sni.shared.schemas import ORMModel


class SkepticJSONModel(BaseModel):
    name: str
    name_slug: str
    title: str
    article: Optional[str] = None
    date: datetime.date
    source: str
    excerpt: Optional[str] = None
    link: str
    media_embed: Optional[str] = None
    twitter_screenshot: Optional[bool] = False
    wayback_link: Optional[str] = None


class SkepticModel(ORMModel):
    name: str
    slug: str
    title: str
    article: Optional[str] = None
    date: datetime.date
    source: str
    excerpt: Optional[str] = None
    link: str
    media_embed: Optional[str] = None
    twitter_screenshot: Optional[bool] = False
    wayback_link: Optional[str] = None

    @field_serializer("date")
    def serialize_date(self, date: datetime.date) -> str:
        return date.isoformat()

    @field_serializer("link")
    def serialize_link(self, link) -> List[str]:
        return [_link.strip() for _link in link.split(",")]
