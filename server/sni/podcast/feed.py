from typing import Sequence

from feedgen.feed import FeedGenerator

from sni.models import Episode
from sni.shared.urls import BaseURLGenerator
from sni.utils.dates import localize_time


class URLGenerator(BaseURLGenerator):
    @property
    def index(self) -> str:
        return f"{self.base_url}/podcast"

    @property
    def rss(self) -> str:
        return f"{self.index}/rss"

    def episode(self, slug: str) -> str:
        return f"{self.index}/{slug}"

    def image(self, filename: str) -> str:
        return f"{self.base_cdn_url}/img/podcast/{filename}"

    def mp3(self, slug: str) -> str:
        return f"{self.base_cdn_url}/cryptomises/{slug}.mp3"


def generate_podcast_feed(
    episodes: Sequence[Episode],
) -> FeedGenerator:
    locale = "en"
    urls = URLGenerator(locale)

    fg = FeedGenerator()
    fg.load_extension("podcast")
    fg.id(urls.index)
    fg.title("The Crypto-Mises Podcast")
    fg.podcast.itunes_author("Satoshi Nakamoto Institute")
    fg.subtitle("The official podcast of the Satoshi Nakamoto Institute")
    fg.link(
        [{"href": urls.rss, "rel": "self"}, {"href": urls.index, "rel": "alternate"}]
    )
    fg.language(locale)
    fg.copyright("cc-by-sa")
    fg.podcast.itunes_summary(
        "Michael Goldstein and Daniel Krawisz of the Satoshi Nakamoto Institute discuss Bitcoin, economics, and cryptography."  # noqa
    )
    fg.podcast.itunes_owner("Michael Goldstein", "michael@bitstein.org")
    fg.generator(generator=None)
    fg.podcast.itunes_explicit("no")
    fg.image(urls.image("cmpodcast_144.jpg"))
    fg.podcast.itunes_image(urls.image("cmpodcast_1440.jpg"))
    fg.podcast.itunes_category("Technology", "Tech News")

    for episode in reversed(episodes):
        description = f"""{episode.notes}
        If you enjoyed this episode, show your support by donating to SNI:
        {urls.donate}"""
        enclosure_url = urls.mp3(episode.slug)

        fe = fg.add_entry()
        fe.id(urls.episode(episode.slug))
        fe.title(episode.title)
        fe.podcast.itunes_summary(description)
        fe.description(description)
        fe.podcast.itunes_subtitle(episode.summary)
        fe.podcast.itunes_author("Satoshi Nakamoto Institute")
        fe.enclosure(enclosure_url, 0, "audio/mpeg")
        fe.podcast.itunes_duration(episode.duration)
        fe.pubDate(localize_time(episode.date))

    return fg
