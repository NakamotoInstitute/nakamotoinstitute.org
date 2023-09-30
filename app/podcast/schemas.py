import datetime

from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class EpisodeMDSchema(BaseModel):
    title: str
    date: datetime.datetime
    duration: str
    summary: str
    notes: str
    youtube_id: str


class EpisodeResponse(EpisodeMDSchema):
    slug: str
    content: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
