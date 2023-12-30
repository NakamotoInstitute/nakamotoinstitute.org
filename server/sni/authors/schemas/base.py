from pydantic import BaseModel, Field

from sni.shared.schemas import ORMModel


class AuthorMDModel(BaseModel):
    name: str
    sort_name: str


class AuthorModel(ORMModel):
    slug: str
    name: str
    sort_name: str
    html_content: str = Field(alias="content")
