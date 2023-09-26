from typing import List

from pydantic import BaseModel

from app.mempool.schemas import MempoolPostBaseSchema

from .base import AuthorSchema


class AuthorResponse(BaseModel):
    author: AuthorSchema
    mempool: List[MempoolPostBaseSchema]
