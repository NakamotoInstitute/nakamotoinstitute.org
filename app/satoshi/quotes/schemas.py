import datetime
from typing import List, Optional

from pydantic import AliasPath, BaseModel, Field, model_validator
from pydantic.alias_generators import to_camel


class QuoteCategoryJSONSchema(BaseModel):
    name: str
    slug: str


class QuoteBaseSchema(BaseModel):
    whitepaper: Optional[bool] = False
    text: str
    post_id: Optional[int] = None
    email_id: Optional[int] = None
    date: datetime.date

    @model_validator(mode="after")
    def check_source(self) -> "QuoteBaseSchema":
        if not self.whitepaper and self.post_id is None and self.email_id is None:
            raise ValueError("Must have a source")
        return self


class QuoteJSONSchema(QuoteBaseSchema):
    categories: List[str]


class QuoteCategoryResponse(QuoteCategoryJSONSchema):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteItem(BaseModel):
    satoshi_id: int
    subject: str
    source: str = Field(alias=AliasPath("thread", "source"))

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteResponse(BaseModel):
    whitepaper: Optional[bool] = False
    text: str
    post: Optional[QuoteItem] = None
    email: Optional[QuoteItem] = None
    date: datetime.date
    categories: List[QuoteCategoryResponse]

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteCategoryDetailResponse(BaseModel):
    category: QuoteCategoryResponse
    quotes: List[QuoteResponse]
