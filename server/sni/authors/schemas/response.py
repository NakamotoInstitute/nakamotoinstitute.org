from typing import List

from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from sni.library.schemas import DocumentBaseModel
from sni.mempool.schemas import MempoolPostBaseModel

from .base import AuthorModel


class AuthorDetailModel(BaseModel):
    author: AuthorModel
    library: List[DocumentBaseModel]
    mempool: List[MempoolPostBaseModel]

    class Config:
        alias_generator = to_camel
