from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from sni.constants import Locales
from sni.library.schemas import DocumentIndexModel
from sni.mempool.schemas import MempoolPostIndexModel

from .base import AuthorModel


class AuthorDetailModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    author: AuthorModel
    library: list[DocumentIndexModel]
    mempool: list[MempoolPostIndexModel]
    locales: list[Locales]
