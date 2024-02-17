from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from sni.constants import Locales
from sni.library.schemas import DocumentIndexModel
from sni.mempool.schemas import MempoolPostIndexModel

from .base import AuthorModel


class AuthorDetailModel(BaseModel):
    author: AuthorModel
    library: list[DocumentIndexModel]
    mempool: list[MempoolPostIndexModel]
    locales: list[Locales]

    class Config:
        alias_generator = to_camel
