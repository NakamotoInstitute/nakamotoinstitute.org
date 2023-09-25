from typing import List

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class PostSchema(BaseModel):
    title: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class AuthorBaseSchema(BaseModel):
    slug: str
    name: str
    sort_name: str
    content: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class AuthorSchema(AuthorBaseSchema, BaseModel):
    posts: List[PostSchema] = Field(flatten=True)

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
