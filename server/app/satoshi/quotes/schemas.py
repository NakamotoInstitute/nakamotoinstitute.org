import datetime
from typing import List, Optional

from pydantic import AliasPath, BaseModel, Field, model_validator
from pydantic.alias_generators import to_camel


class QuoteCategoryJSONModel(BaseModel):
    name: str
    slug: str


class QuoteBaseModel(BaseModel):
    whitepaper: Optional[bool] = False
    text: str
    post_id: Optional[int] = None
    email_id: Optional[int] = None
    date: datetime.date

    @model_validator(mode="after")
    def check_source(self) -> "QuoteBaseModel":
        if not self.whitepaper and self.post_id is None and self.email_id is None:
            raise ValueError("Must have a source")
        return self


class QuoteJSONModel(QuoteBaseModel):
    categories: List[str]


class QuoteCategoryBaseModel(QuoteCategoryJSONModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteItemModel(BaseModel):
    satoshi_id: int
    subject: str
    source: str = Field(alias=AliasPath("thread", "source"))

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteModel(BaseModel):
    whitepaper: Optional[bool] = False
    text: str
    post: Optional[QuoteItemModel] = None
    email: Optional[QuoteItemModel] = None
    date: datetime.date
    categories: List[QuoteCategoryBaseModel]

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteCategoryModel(BaseModel):
    category: QuoteCategoryBaseModel
    quotes: List[QuoteModel]
