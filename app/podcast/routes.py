from feedgen.feed import FeedGenerator
from flask import make_response, redirect, render_template, url_for
from sqlalchemy import asc, desc

from app import cache
from app.models import Episode
from app.podcast import bp
from app.utils import localize_time


@bp.route("/", methods=["GET"])
@cache.cached()
def index():
    episodes = Episode.query.order_by(desc(Episode.date)).all()
    return render_template("podcast/index.html", episodes=episodes)


@bp.route("/<string:slug>/", methods=["GET"])
@cache.cached()
def detail(slug):
    episode = Episode.query.filter_by(slug=slug).order_by(desc(Episode.date)).first()
    if episode is not None:
        return render_template(f"podcast/episodes/{slug}.html", episode=episode)
    else:
        return redirect(url_for("podcast.index"))


@bp.route("/feed/", methods=["GET"])
@cache.cached()
def feed():
    # Entries are added backwards
    episodes = Episode.query.order_by(asc(Episode.date)).all()

    fg = FeedGenerator()
    fg.load_extension("podcast")
    fg.title("The Crypto-Mises Podcast")
    fg.podcast.itunes_author("Satoshi Nakamoto Institute")
    fg.link(href=url_for("main.index", _external=True), rel="alternate")
    fg.subtitle("The official podcast of the Satoshi Nakamoto Institute")
    fg.language("en")
    fg.copyright("cc-by-sa")
    fg.podcast.itunes_summary(
        "Michael Goldstein and Daniel Krawisz of the Satoshi Nakamoto Institute discuss Bitcoin, economics, and cryptography."  # noqa
    )
    fg.podcast.itunes_owner("Michael Goldstein", "michael@bitstein.org")
    fg.link(href=url_for("podcast.feed", _external=True), rel="self")
    fg.podcast.itunes_explicit("no")
    fg.image(url_for("static", filename="img/cryptomises/cmpodcast_144.jpg"))
    fg.podcast.itunes_image(
        url_for("static", filename="img/cryptomises/cmpodcast_1440.jpg")
    )
    fg.podcast.itunes_category("Technology", "Tech News")

    for episode in episodes:
        description = f"""{episode.summary}
        If you enjoyed this episode, show your support by donating to SNI:
        {url_for('main.donate', _external=True)}"""
        enclosure_url = (
            f"https://s3.amazonaws.com/nakamotoinstitute/cryptomises/{episode.slug}.mp3"
        )

        fe = fg.add_entry()
        fe.id(url_for("podcast.detail", slug=episode.slug, _external=True))
        fe.title(episode.title)
        fe.podcast.itunes_summary(description)
        fe.description(description)
        fe.podcast.itunes_subtitle(episode.subtitle)
        fe.podcast.itunes_author("Satoshi Nakamoto Institute")
        fe.enclosure(enclosure_url, 0, "audio/mpeg")
        fe.podcast.itunes_duration(episode.duration)
        fe.pubDate(localize_time(episode.time))

    response = make_response(fg.rss_str(encoding="utf-8", pretty=True))
    response.headers.set("Content-Type", "application/rss+xml")
    return response
