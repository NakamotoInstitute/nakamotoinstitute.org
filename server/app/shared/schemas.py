from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class SlugParamModel(BaseModel):
    slug: str
    locale: str


class TranslationSchema(BaseModel):
    locale: str
    title: str
    slug: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
