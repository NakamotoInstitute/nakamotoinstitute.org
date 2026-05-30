import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class SearchModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class SearchResult(SearchModel):
    entity_type: str
    category: str
    title: str
    snippet: str
    ref: dict
    date: datetime.date | None = None
    rank: float


class CountsByCategory(SearchModel):
    satoshi: int = 0
    library: int = 0
    mempool: int = 0
    authors: int = 0
    podcasts: int = 0


class SearchResponse(SearchModel):
    query: str
    total: int
    counts_by_category: CountsByCategory
    results: list[SearchResult]
