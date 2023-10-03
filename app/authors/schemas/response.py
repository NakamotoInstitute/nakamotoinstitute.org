from typing import List

from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from app.library.schemas import LibraryDocBaseSchema
from app.mempool.schemas import MempoolPostBaseSchema

from .base import AuthorSchema


class AuthorResponse(BaseModel):
    author: AuthorSchema
    library: List[LibraryDocBaseSchema]
    mempool: List[MempoolPostBaseSchema]

    class Config:
        alias_generator = to_camel
