from typing import List

from feedgen.feed import FeedGenerator

from sni.constants import LocaleType
from sni.models import BlogPostTranslation
from sni.shared.feed import FeedFormat
from sni.shared.urls import BaseURLGenerator
from sni.utils.dates import date_to_localized_datetime


class URLGenerator(BaseURLGenerator):
    @property
    def index(self) -> str:
        return f"{self.base_url}/mempool"

    @property
    def rss(self) -> str:
        return f"{self.index}/rss"

    @property
    def atom(self) -> str:
        return f"{self.index}/atom"

    def post(self, slug: str) -> str:
        return f"{self.index}/{slug}"


def generate_mempool_feed(
    posts: List[BlogPostTranslation],
    locale: LocaleType = "en",
    format: FeedFormat = FeedFormat.rss,
) -> FeedGenerator:
    urls = URLGenerator(locale)
    feed_url = getattr(urls, format.value, urls.rss)

    fg = FeedGenerator()
    fg.id(urls.index)
    fg.updated(date_to_localized_datetime(posts[0].blog_post.added))
    fg.title("The Memory Pool | Satoshi Nakamoto Institute")
    fg.subtitle(
        "Where ideas wait to be mined into the block chain of the collective conscience"
    )
    fg.link(
        [{"href": feed_url, "rel": "self"}, {"href": urls.index, "rel": "alternate"}]
    )
    fg.language(locale)
    fg.generator(generator=None)

    for post in reversed(posts):
        authors = post.blog_post.authors

        fe = fg.add_entry()
        fe.load_extension("dc", rss=True)
        fe.id(urls.post(post.slug))
        fe.guid(urls.post(post.slug), permalink=True)
        fe.link(href=urls.post(post.slug))
        fe.title(post.title)
        fe.published(date_to_localized_datetime(post.blog_post.added))
        fe.dc.dc_creator(creator=[author.name for author in authors])
        fe.author([{"name": author.name} for author in authors])
        fe.description(post.excerpt)
        fe.content(post.html_content)

    return fg
