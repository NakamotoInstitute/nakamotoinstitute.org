from datetime import datetime

from feedgen.feed import FeedGenerator
from flask import make_response, redirect, render_template, url_for
from pytz import timezone
from sqlalchemy import asc, desc

from app import cache, pages
from app.mempool import bp
from app.models import BlogPost, Language

TIMEZONE = timezone("US/Central")


def date_to_localized_datetime(date):
    time = datetime(year=date.year, month=date.month, day=date.day)
    return TIMEZONE.localize(time)


@bp.route("/", methods=["GET"])
@cache.cached()
def index():
    blog_posts = BlogPost.query.order_by(desc(BlogPost.added)).all()
    return render_template("mempool/index.html", blog_posts=blog_posts)


@bp.route("/<string:slug>/", methods=["GET"])
@cache.cached()
def detail(slug):
    # Redirect for new appcoin slug
    if slug == "appcoins-are-fraudulent":
        return redirect(url_for("mempool.detail", slug="appcoins-are-snake-oil"))
    blog_post = (
        BlogPost.query.filter_by(slug=slug).order_by(desc(BlogPost.date)).first()
    )
    if blog_post:
        english = Language.query.filter_by(ietf="en").first()
        page = pages.get(f"mempool/{slug}")
        translations = [translation.language for translation in blog_post.translations]
        translations.sort(key=lambda t: t.name)
        previous_post = next_post = None
        if blog_post.series:
            previous_post = BlogPost.query.filter_by(
                series=blog_post.series, series_index=blog_post.series_index - 1
            ).first()
            next_post = BlogPost.query.filter_by(
                series=blog_post.series, series_index=blog_post.series_index + 1
            ).first()
        return render_template(
            "mempool/detail.html",
            blog_post=blog_post,
            page=page,
            language=english,
            translations=translations,
            previous_post=previous_post,
            next_post=next_post,
        )
    else:
        return redirect(url_for("mempool.index"))


@bp.route("/<string:slug>/<string:language>/", methods=["GET"])
@cache.cached()
def detail_translation(slug, language):
    blog_post = (
        BlogPost.query.filter_by(slug=slug).order_by(desc(BlogPost.date)).first()
    )
    language_lower = language.lower()
    if blog_post is not None:
        if language_lower == "en":
            return redirect(url_for("mempool.detail", slug=slug))
        elif language != language_lower:
            return redirect(
                url_for(
                    "mempool.detail_translation", slug=slug, language=language_lower
                )
            )
        post_language = Language.query.filter_by(ietf=language_lower).first()
        if post_language not in [
            translation.language for translation in blog_post.translations
        ]:
            return redirect(url_for("mempool.detail", slug=slug))
        else:
            page = pages.get(f"mempool/{slug}-{language}")
            rtl = False
            if language in ["ar", "fa", "he"]:
                rtl = True
            translations = [Language.query.get(1)]
            translators = None
            blog_post_translations = blog_post.translations
            blog_post_translations.sort(key=lambda x: x.language.name)
            for translation in blog_post_translations:
                if translation.language.ietf != language_lower:
                    translations.append(translation.language)
                else:
                    translators = translation.translators
            return render_template(
                "mempool/detail.html",
                blog_post=blog_post,
                page=page,
                language=post_language,
                rtl=rtl,
                translations=translations,
                translators=translators,
            )
    else:
        return redirect(url_for("mempool.index"))


@bp.route("/feed/")
@cache.cached()
def feed():
    # Entries are added backwards
    articles = BlogPost.query.order_by(asc(BlogPost.added)).all()

    fg = FeedGenerator()
    fg.title("Mempool | Satoshi Nakamoto Institute")
    fg.id("https://nakamotoinstitute.org/mempool/feed/")
    fg.updated(date_to_localized_datetime(articles[0].added))
    fg.link(href="https://nakamotoinstitute.org")
    fg.link(href="https://nakamotoinstitute.org/mempool/feed/", rel="self")
    fg.language("en")

    for article in articles:
        url = url_for("mempool.detail", slug=article.slug, _external=True)
        page = pages.get(f"mempool/{article.slug}")

        fe = fg.add_entry()
        fe.id(url)
        fe.title(article.title)
        fe.link(href=url)
        fe.updated(date_to_localized_datetime(article.added))
        fe.published(date_to_localized_datetime(article.date))
        fe.author(name=str(article.author[0]))
        fe.content(page.html)

    response = make_response(fg.atom_str(encoding="utf-8", pretty=True))
    response.headers.set("Content-Type", "application/atom+xml")
    return response
