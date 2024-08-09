import datetime
from typing import Optional

from pydantic import AliasPath, BaseModel, Field, model_validator
from pydantic.alias_generators import to_camel

from sni.shared.schemas import IteratableRootModel, ORMModel


class QuoteCategoryJSONModel(BaseModel):
    name: str
    slug: str


class QuoteCategoriesJSONModel(IteratableRootModel):
    root: list[QuoteCategoryJSONModel]


class QuoteBaseModel(BaseModel):
    whitepaper: bool = False
    text: str
    post_id: int | None = None
    email_id: int | None = None
    date: datetime.date

    @model_validator(mode="after")
    def check_source(self) -> "QuoteBaseModel":
        if not self.whitepaper and self.post_id is None and self.email_id is None:
            raise ValueError("Must have a source")
        return self


class QuoteJSONModel(QuoteBaseModel):
    categories: list[str]


class QuotesJSONModel(IteratableRootModel):
    root: list[QuoteJSONModel]


class QuoteCategoryBaseModel(QuoteCategoryJSONModel, ORMModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteItemModel(BaseModel):
    satoshi_id: int
    subject: str
    source: str = Field(validation_alias=AliasPath("thread", "source"))

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteModel(BaseModel):
    whitepaper: bool = False
    text: str
    post: Optional[QuoteItemModel] = None
    email: Optional[QuoteItemModel] = None
    date: datetime.date
    categories: list[QuoteCategoryBaseModel]

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class QuoteCategoryModel(BaseModel):
    category: QuoteCategoryBaseModel
    quotes: list[QuoteModel]
