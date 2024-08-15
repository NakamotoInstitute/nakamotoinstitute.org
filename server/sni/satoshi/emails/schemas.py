import datetime
from typing import Literal

from pydantic import AliasPath, BaseModel, Field, field_serializer
from pydantic.alias_generators import to_camel

from sni.shared.schemas import IterableRootModel, ORMModel

EmailSource = Literal["cryptography", "bitcoin-list", "p2p-research"]


class EmailThreadJSONModel(BaseModel):
    id: int
    title: str
    source: EmailSource
    url: str
    date: datetime.datetime


class EmailThreadsJSONModel(IterableRootModel):
    root: list[EmailThreadJSONModel]


class EmailJSONModel(BaseModel):
    id: int
    sent_from: str
    subject: str
    text: str
    date: datetime.datetime
    url: str
    thread_id: int
    source_id: str
    parent_id: int | None = None
    satoshi_id: int | None = None


class EmailsJSONModel(IterableRootModel):
    root: list[EmailJSONModel]


class EmailThreadBaseModel(EmailThreadJSONModel, ORMModel):
    date: datetime.datetime
    url: str


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
    parent_id: int | None
    satoshi_id: int | None
    source: str = Field(validation_alias=AliasPath("thread", "source"))
    replies: list[EmailReplyModel]

    @field_serializer("date")
    def serialize_date(self, date: datetime.date) -> str:
        return date.isoformat()

    @field_serializer("replies")
    def serialize_replies(self, replies) -> list[str]:
        """Convert EmailReplyModel to source_id string."""
        return sorted([reply.source_id for reply in replies])


class ThreadEmailModel(EmailBaseModel):
    parent: EmailBaseModel | None


class EmailThreadModel(BaseModel):
    emails: list[ThreadEmailModel]
    thread: EmailThreadBaseModel
    previous: EmailThreadBaseModel | None
    next: EmailThreadBaseModel | None

    class Config:
        alias_generator = to_camel


class SatoshiEmailModel(EmailBaseModel):
    satoshi_id: int


class EmailDetailModel(BaseModel):
    email: SatoshiEmailModel
    previous: SatoshiEmailModel | None
    next: SatoshiEmailModel | None

    class Config:
        alias_generator = to_camel
