import datetime
from typing import List, Optional

from pydantic import BaseModel


class QuoteCategoryJSONSchema(BaseModel):
    name: str
    slug: str


class QuoteJSONSchema(BaseModel):
    medium: str
    text: str
    post_id: Optional[int] = None
    email_id: Optional[int] = None
    date: datetime.date
    categories: List[str]
