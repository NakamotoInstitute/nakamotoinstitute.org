from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from sni.constants import Locales


class ORMModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class SlugParamModel(BaseModel):
    slug: str
    locale: Locales


class TranslationSchema(ORMModel):
    locale: Locales
    title: str
    slug: str
