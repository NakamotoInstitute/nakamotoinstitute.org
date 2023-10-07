from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class AuthorMDModel(BaseModel):
    name: str
    sort_name: str


class AuthorModel(BaseModel):
    slug: str
    name: str
    sort_name: str
    content: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
