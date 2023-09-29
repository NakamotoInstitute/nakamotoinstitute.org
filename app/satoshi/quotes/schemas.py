import datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class QuoteCategoryJSONSchema(BaseModel):
    name: str
    slug: str


class QuoteBaseSchema(BaseModel):
    medium: str
    text: str
    post_id: Optional[int] = None
    email_id: Optional[int] = None
    date: datetime.date


class QuoteJSONSchema(QuoteBaseSchema):
    categories: List[str]


class QuoteCategoryResponse(QuoteCategoryJSONSchema):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteResponse(QuoteBaseSchema):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteCategoryDetailResponse(BaseModel):
    category: QuoteCategoryResponse
    quotes: List[QuoteResponse]
