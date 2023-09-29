import datetime
from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, Field
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
    emails: List["EmailBaseResponse"]
    thread: EmailThreadResponse
    previous: Optional[EmailThreadResponse]
    next: Optional[EmailThreadResponse]

    class Config:
        alias_generator = to_camel


class EmailBaseResponse(EmailJSONSchema):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class EmailResponse(EmailBaseResponse):
    parent: Optional[EmailBaseResponse]


class EmailDetailResponse(BaseModel):
    email: EmailBaseResponse
    previous: Optional[EmailBaseResponse]
    next: Optional[EmailBaseResponse]

    class Config:
        alias_generator = to_camel
