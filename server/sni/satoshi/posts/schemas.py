import datetime
from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, Field, field_validator
from pydantic.alias_generators import to_camel

from sni.shared.schemas import ORMModel

ForumPostSource = Literal["p2pfoundation", "bitcointalk"]


class ForumThreadJSONModel(BaseModel):
    id: int
    title: str
    source: ForumPostSource


class ForumPostJSONModel(BaseModel):
    id: int
    poster_name: str
    poster_url: Optional[str] = None
    subject: str
    text: str
    date: datetime.datetime
    url: str
    thread_id: int
    source_id: str
    nested_level: int = 0
    satoshi_id: Optional[int] = None

    @field_validator("nested_level")
    @classmethod
    def nested_level_must_be_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("must be positive")
        return v

    @field_validator("satoshi_id")
    @classmethod
    def satoshi_id_must_be_gte_one(cls, v: int) -> int:
        if v and v < 1:
            raise ValueError("must be greater than or equal to 1")
        return v


class ForumPostBaseModel(ORMModel):
    poster_name: str
    poster_url: Optional[str] = None
    subject: str
    text: str
    date: datetime.datetime
    url: str
    thread_id: int
    source_id: str
    nested_level: int = 0
    satoshi_id: Optional[int] = None
    source: str = Field(alias=AliasPath("thread", "source"))


class ForumThreadBaseModel(ForumThreadJSONModel, ORMModel):
    date: datetime.datetime = Field(alias=AliasPath("posts", 0, "date"))


class ForumPostModel(ForumPostBaseModel):
    pass


class ForumThreadModel(BaseModel):
    posts: List[ForumPostModel]
    thread: ForumThreadBaseModel
    previous: Optional[ForumThreadBaseModel]
    next: Optional[ForumThreadBaseModel]

    class Config:
        alias_generator = to_camel


class SatoshiForumPostModel(ForumPostBaseModel):
    satoshi_id: int


class ForumPostDetailModel(BaseModel):
    post: SatoshiForumPostModel
    previous: Optional[SatoshiForumPostModel]
    next: Optional[SatoshiForumPostModel]

    class Config:
        alias_generator = to_camel
