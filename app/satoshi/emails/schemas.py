import datetime
from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, Field, field_serializer
from pydantic.alias_generators import to_camel

EmailSource = Literal["cryptography", "bitcoin-list"]


class EmailThreadJSONSchema(BaseModel):
    id: int
    title: str
    source: EmailSource


class EmailJSONSchema(BaseModel):
    id: int
    sent_from: str
    subject: str
    text: str
    date: datetime.datetime
    url: str
    thread_id: int
    source_id: str
    parent_id: Optional[int] = None
    satoshi_id: Optional[int] = None


class EmailThreadResponse(EmailThreadJSONSchema):
    date: datetime.datetime = Field(alias=AliasPath("emails", 0, "date"))

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class EmailThreadDetailResponse(BaseModel):
    emails: List["ThreadEmailResponse"]
    thread: EmailThreadResponse
    previous: Optional[EmailThreadResponse]
    next: Optional[EmailThreadResponse]

    class Config:
        alias_generator = to_camel


class EmailReplyResponse(BaseModel):
    source_id: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class EmailBaseResponse(BaseModel):
    sent_from: str
    subject: str
    text: str
    date: datetime.datetime
    url: str
    thread_id: int
    source_id: str
    parent_id: Optional[int] = None
    satoshi_id: Optional[int] = None
    source: str = Field(alias=AliasPath("thread", "source"))
    replies: List[EmailReplyResponse]

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True

    @field_serializer("date")
    def serialize_date(self, date: datetime.date) -> str:
        return date.isoformat()

    @field_serializer("replies")
    def serialize_replies(self, replies) -> List[str]:
        """Convert EmailReplyResponse to source_id string."""
        return sorted([reply.source_id for reply in replies])


class ThreadEmailResponse(EmailBaseResponse):
    parent: Optional[EmailBaseResponse]


class EmailResponse(EmailBaseResponse):
    satoshi_id: int


class EmailDetailResponse(BaseModel):
    email: EmailResponse
    previous: Optional[EmailBaseResponse] = None
    next: Optional[EmailBaseResponse] = None

    class Config:
        alias_generator = to_camel
