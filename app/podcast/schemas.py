import datetime

from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class EpisodeMDModel(BaseModel):
    title: str
    date: datetime.datetime
    duration: str
    summary: str
    notes: str
    youtube_id: str


class EpisodeModel(EpisodeMDModel):
    slug: str
    content: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
