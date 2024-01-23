import datetime
from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, Field, field_serializer
from pydantic.alias_generators import to_camel

from sni.shared.schemas import ORMModel

EmailSource = Literal["cryptography", "bitcoin-list"]


class EmailThreadJSONModel(BaseModel):
    id: int
    title: str
    source: EmailSource


class EmailJSONModel(BaseModel):
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


class EmailThreadBaseModel(EmailThreadJSONModel, ORMModel):
    date: datetime.datetime = Field(alias=AliasPath("emails", 0, "date"))
    url: str = Field(alias=AliasPath("emails", 0, "url"))


class EmailReplyModel(ORMModel):
    source_id: str


class EmailBaseModel(ORMModel):
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
    replies: List[EmailReplyModel]

    @field_serializer("date")
    def serialize_date(self, date: datetime.date) -> str:
        return date.isoformat()

    @field_serializer("replies")
    def serialize_replies(self, replies) -> List[str]:
        """Convert EmailReplyModel to source_id string."""
        return sorted([reply.source_id for reply in replies])


class ThreadEmailModel(EmailBaseModel):
    parent: Optional[EmailBaseModel]


class EmailThreadModel(BaseModel):
    emails: List[ThreadEmailModel]
    thread: EmailThreadBaseModel
    previous: Optional[EmailThreadBaseModel]
    next: Optional[EmailThreadBaseModel]

    class Config:
        alias_generator = to_camel


class SatoshiEmailModel(EmailBaseModel):
    satoshi_id: int


class EmailDetailModel(BaseModel):
    email: SatoshiEmailModel
    previous: Optional[SatoshiEmailModel] = None
    next: Optional[SatoshiEmailModel] = None

    class Config:
        alias_generator = to_camel
