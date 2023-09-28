from typing import Optional

from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class TranslatorBaseSchema(BaseModel):
    name: str
    url: Optional[str] = None


class TranslatorMDSchema(TranslatorBaseSchema):
    pass


class TranslatorSchema(TranslatorBaseSchema):
    slug: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
