import datetime

from pydantic import AliasPath, BaseModel, Field

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
    html_content: str = Field(
        validation_alias=AliasPath("content", "html_content"), alias="content"
    )
