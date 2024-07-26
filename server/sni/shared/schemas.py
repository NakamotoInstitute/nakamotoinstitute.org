from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from sni.constants import Locales


class ORMModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class SlugParamModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )

    slug: str
    locale: Locales


class TranslationSchema(ORMModel):
    locale: Locales
    title: str
    slug: str
