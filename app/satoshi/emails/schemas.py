import datetime
from typing import Literal, Optional

from pydantic import BaseModel
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


class EmailBaseResponse(EmailJSONSchema):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class EmailResponse(EmailBaseResponse):
    parent: Optional[EmailBaseResponse]
