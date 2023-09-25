import datetime
from typing import Optional

from pydantic import BaseModel


class AuthorMDSchema(BaseModel):
    name: str
    sort_name: str


class MempoolMDSchema(BaseModel):
    title: str
    excerpt: str
    author: str
    image: Optional[str] = None
    image_alt: Optional[str] = None
    date: datetime.date
    added: Optional[datetime.date] = None
    original_url: Optional[str] = None
    original_site: Optional[str] = None


class MempoolTranslatedMDSchema(BaseModel):
    title: str
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    image_alt: Optional[str] = None
    translation_url: Optional[str] = None
    translation_site: Optional[str] = None
    translation_site_url: Optional[str] = None
