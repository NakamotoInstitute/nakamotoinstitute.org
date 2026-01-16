import datetime

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_serializer
from pydantic.alias_generators import to_camel

from sni.constants import EmailSource
from sni.shared.schemas import IterableRootModel, ORMModel


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
    disclaimer: str | None = None
    thread_id: int
    source_id: str
    parent_id: int | None = None
    satoshi_id: int | None = None


class EmailsJSONModel(IterableRootModel):
    root: list[EmailJSONModel]


class EmailThreadBase(EmailThreadJSONModel, ORMModel):
    pass


class EmailReply(ORMModel):
    source_id: str


class EmailBase(ORMModel):
    sent_from: str
    subject: str
    text: str
    date: datetime.datetime
    url: str
    disclaimer: str | None = None
    thread_id: int
    source_id: str
    parent_id: int | None
    satoshi_id: int | None
    source: EmailSource = Field(validation_alias=AliasPath("thread", "source"))
    replies: list[EmailReply]

    @field_serializer("replies")
    def serialize_replies(self, replies) -> list[str]:
        """Convert EmailReply to source_id string."""
        return sorted([reply.source_id for reply in replies])


class ThreadEmail(EmailBase):
    parent: EmailBase | None


class EmailThread(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    emails: list[ThreadEmail]
    thread: EmailThreadBase
    previous: EmailThreadBase | None
    next: EmailThreadBase | None


class SatoshiEmail(EmailBase):
    satoshi_id: int


class EmailDetail(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    email: SatoshiEmail
    previous: SatoshiEmail | None
    next: SatoshiEmail | None
