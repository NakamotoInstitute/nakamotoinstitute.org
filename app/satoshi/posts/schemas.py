import datetime
from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, Field, field_validator
from pydantic.alias_generators import to_camel

EmailSource = Literal["p2pfoundation", "bitcointalk"]


class ForumThreadJSONSchema(BaseModel):
    id: int
    title: str
    source: EmailSource


class ForumPostJSONSchema(BaseModel):
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


class ForumPostBaseResponse(BaseModel):
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

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class ForumThreadResponse(ForumThreadJSONSchema):
    date: datetime.datetime = Field(alias=AliasPath("posts", 0, "date"))

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class ForumThreadDetailResponse(BaseModel):
    posts: List["ForumPostResponse"]
    thread: ForumThreadResponse
    previous: Optional[ForumThreadResponse]
    next: Optional[ForumThreadResponse]

    class Config:
        alias_generator = to_camel


class ForumPostResponse(ForumPostBaseResponse):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class ForumPostDetailResponse(BaseModel):
    post: ForumPostResponse
    previous: Optional[ForumPostResponse]
    next: Optional[ForumPostResponse]

    class Config:
        alias_generator = to_camel
