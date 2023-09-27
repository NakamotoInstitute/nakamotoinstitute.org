from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class TranslatorBaseSchema(BaseModel):
    name: str
    url: str
    slug: str


class TranslatorMDSchema(TranslatorBaseSchema):
    pass


class TranslatorSchema(TranslatorBaseSchema):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
