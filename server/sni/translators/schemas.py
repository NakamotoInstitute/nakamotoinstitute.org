from typing import Optional

from pydantic import BaseModel

from sni.shared.schemas import ORMModel


class TranslatorBaseModel(BaseModel):
    name: str
    url: Optional[str] = None


class TranslatorMDModel(TranslatorBaseModel):
    pass


class TranslatorModel(TranslatorBaseModel, ORMModel):
    slug: str
