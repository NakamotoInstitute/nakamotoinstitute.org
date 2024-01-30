from typing import List

from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from sni.config import Locales
from sni.library.schemas import DocumentIndexModel
from sni.mempool.schemas import MempoolPostIndexModel

from .base import AuthorModel


class AuthorDetailModel(BaseModel):
    author: AuthorModel
    library: List[DocumentIndexModel]
    mempool: List[MempoolPostIndexModel]
    locales: List[Locales]

    class Config:
        alias_generator = to_camel
