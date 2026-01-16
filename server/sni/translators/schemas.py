from pydantic import BaseModel

from sni.shared.schemas import ORMModel


class TranslatorBaseModel(BaseModel):
    name: str
    url: str | None = None


class TranslatorMDModel(TranslatorBaseModel):
    pass


class Translator(TranslatorBaseModel, ORMModel):
    slug: str
