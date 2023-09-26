from typing import List

from pydantic import BaseModel

from app.library.schemas import LibraryDocBaseSchema
from app.mempool.schemas import MempoolPostBaseSchema

from .base import AuthorSchema


class AuthorResponse(BaseModel):
    author: AuthorSchema
    library: List[LibraryDocBaseSchema]
    mempool: List[MempoolPostBaseSchema]
