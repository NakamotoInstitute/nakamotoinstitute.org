import datetime

from pydantic import BaseModel

from sni.shared.schemas import ORMModel


class EpisodeMDModel(BaseModel):
    title: str
    date: datetime.datetime
    duration: str
    summary: str
    notes: str
    youtube_id: str


class EpisodeModel(EpisodeMDModel, ORMModel):
    slug: str
    content: str
