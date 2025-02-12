from feedgen.feed import FeedGenerator

from sni.config import settings
from sni.models import Episode, Podcast
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


def generate_description(episode: Episode, urls: URLGenerator) -> str:
    return f"""{episode.notes}
    If you enjoyed this episode, show your support by donating to SNI:
    {urls.donate}"""


def generate_podcast_feed(
    podcast: Podcast,
) -> FeedGenerator:
    locale = "en"
    urls = URLGenerator(locale)

    fg = FeedGenerator()
    fg.load_extension("podcast")
    fg.id(urls.index)
    fg.title(podcast.name)
    fg.description(podcast.description_short)
    fg.podcast.itunes_author(settings.SITE_NAME)
    fg.podcast.itunes_subtitle(podcast.description_short)
    fg.podcast.itunes_summary(podcast.description)
    fg.link(
        [{"href": urls.rss, "rel": "self"}, {"href": urls.index, "rel": "alternate"}]
    )
    fg.language(locale)
    fg.copyright("cc-by-sa")
    fg.podcast.itunes_summary(podcast.summary)
    fg.podcast.itunes_owner(settings.SITE_ADMIN_NAME, settings.SITE_ADMIN_EMAIL)
    fg.generator(generator=None)
    fg.podcast.itunes_explicit("no")
    fg.image(urls.image(podcast.image_small))
    fg.podcast.itunes_image(urls.image(podcast.image_large))
    fg.podcast.itunes_category(podcast.category, podcast.subcategory)

    for episode in reversed(podcast.episodes):
        ep_description = generate_description(episode, urls)
        enclosure_url = urls.mp3(episode.slug)

        fe = fg.add_entry()
        fe.id(urls.episode(episode.slug))
        fe.title(episode.title)
        fe.podcast.itunes_summary(ep_description)
        fe.description(ep_description)
        fe.podcast.itunes_subtitle(episode.summary)
        fe.podcast.itunes_author(settings.SITE_NAME)
        fe.enclosure(enclosure_url, 0, "audio/mpeg")
        fe.podcast.itunes_duration(episode.duration)
        fe.pubDate(localize_time(episode.date))

    return fg
