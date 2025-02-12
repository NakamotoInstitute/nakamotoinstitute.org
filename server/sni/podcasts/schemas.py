import datetime

from pydantic import AliasPath, BaseModel, Field

from sni.shared.schemas import ORMModel


class PodcastMDModel(BaseModel):
    name: str
    sort_name: str
    description: str
    description_short: str | None = None
    image_small: str | None = None
    image_large: str | None = None
    category: str | None = None
    subcategory: str | None = None
    defunct: bool = False
    external_feed: str | None = None
    spotify_url: str | None = None
    apple_podcasts_url: str | None = None
    on_youtube: bool = False
    on_rumble: bool = False


class EpisodeMDModel(BaseModel):
    podcast: str
    title: str
    date: datetime.datetime
    duration: str | None = None
    summary: str | None = None
    notes: str | None = None
    mp3_url: str | None = None
    youtube_id: str | None = None
    rumble_id: str | None = None
    episode_number: int | None = None


class BasePodcastModel(ORMModel):
    slug: str
    name: str
    sort_name: str
    description: str
    description_short: str | None
    external_feed: str | None
    defunct: bool


class PodcastModel(BasePodcastModel):
    spotify_url: str | None
    apple_podcasts_url: str | None
    on_youtube: bool
    on_rumble: bool


class PodcastDetailModel(PodcastModel):
    episodes: list["BaseEpisodeModel"]


class EpisodeParams(ORMModel):
    podcast_slug: str = Field(validation_alias=AliasPath("podcast", "slug"))
    episode_slug: str = Field(validation_alias=AliasPath("slug"))


class BaseEpisodeModel(ORMModel):
    slug: str
    title: str
    date: datetime.datetime
    summary: str | None


class EpisodeModel(EpisodeMDModel, ORMModel):
    slug: str
    html_content: str = Field(
        validation_alias=AliasPath("content", "html_content"), alias="content"
    )
    podcast: PodcastModel
    mp3_url: str | None
    episode_number: int | None
