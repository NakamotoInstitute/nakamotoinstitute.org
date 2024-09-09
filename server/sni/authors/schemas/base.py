from pydantic import BaseModel

from sni.shared.schemas import ORMModel


class AuthorMDModel(BaseModel):
    name: str
    sort_name: str


class AuthorModel(ORMModel):
    slug: str
    name: str
    sort_name: str
