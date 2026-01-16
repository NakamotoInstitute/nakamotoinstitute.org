from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from sni.constants import Locale
from sni.library.schemas import DocumentIndex
from sni.mempool.schemas import MempoolPostIndex

from .base import Author


class AuthorDetail(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    author: Author
    library: list[DocumentIndex]
    mempool: list[MempoolPostIndex]
    locales: list[Locale]
