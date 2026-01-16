from pydantic import AliasGenerator, BaseModel, ConfigDict, RootModel
from pydantic.alias_generators import to_camel

from sni.constants import Locale


class ORMModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class IterableRootModel(RootModel):
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, idx: int):
        return self.root[idx]


class SlugParam(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel)
    )

    slug: str
    locale: Locale


class TranslationSchema(ORMModel):
    locale: Locale
    title: str
    slug: str


class Error(BaseModel):
    detail: str
