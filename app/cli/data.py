import json
import os.path
from datetime import datetime

import click
import requests
import sqlalchemy as sa
from dateutil import parser
from flask import Blueprint

from app import db
from app.cli.skeptics import API_URL, update_skeptics
from app.cli.utils import DONE, color_text
from app.models import (
    Author,
    BlogPost,
    BlogPostTranslation,
    BlogSeries,
    Category,
    Doc,
    Email,
    EmailThread,
    Episode,
    Format,
    ForumThread,
    Language,
    Post,
    Price,
    Quote,
    QuoteCategory,
    ResearchDoc,
    Skeptic,
    Translator,
)

bp = Blueprint("data", __name__)

bp.cli.help = "Update database."


def model_exists(model_class):
    engine = db.get_engine()
    insp = sa.inspect(engine)
    return insp.has_table(model_class.__tablename__)


def get(model, **kwargs):
    return db.session.query(model).filter_by(**kwargs).first()


# See if object already exists for uniqueness
def get_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        return instance


def flush_db():
    click.echo("Initializing database...", nl=False)
    db.drop_all()
    db.create_all()
    click.echo(DONE)


def export_prices():
    if not model_exists(Price):
        return
    click.echo("Exporting Prices...", nl=False)
    prices = Price.query.all()
    serialized_prices = [price.serialize() for price in prices]
    with open("data/prices.json", "w") as f:
        json.dump(serialized_prices, f, indent=4)
    click.echo(DONE)


def import_prices():
    click.echo("Importing Prices...", nl=False)
    prices = []
    fname = "data/prices.json"
    if os.path.isfile(fname):
        with open("data/prices.json") as data_file:
            prices = json.load(data_file)

    if not prices:
        click.echo("Fetching Prices...", nl=False)
        resp = requests.get(API_URL).json()
        click.echo("Adding Prices...", nl=False)
        series = resp["data"]
        for se in series:
            date = parser.parse(se["time"])
            price = se["PriceUSD"]
            new_price = Price(
                date=date,
                price=price,
            )
            db.session.add(new_price)
    else:
        for price in prices:
            new_price = Price(
                date=parser.parse(price["date"]),
                price=price["price"],
            )
            db.session.add(new_price)
    db.session.commit()
    click.echo(DONE)


def import_language():
    click.echo("Importing Language...", nl=False)
    with open("data/languages.json") as data_file:
        languages = json.load(data_file)

    for language in languages:
        new_language = Language(name=language["name"], ietf=language["ietf"])
        db.session.add(new_language)
    db.session.commit()
    click.echo(DONE)


def import_translator():
    click.echo("Importing Translator...", nl=False)
    with open("data/translators.json") as data_file:
        translators = json.load(data_file)

    for translator in translators:
        new_translator = Translator(name=translator["name"], url=translator["url"])
        db.session.add(new_translator)
    db.session.commit()
    click.echo(DONE)


def import_email_thread():
    click.echo("Importing EmailThread...", nl=False)
    with open("data/threads_emails.json") as data_file:
        threads = json.load(data_file)

    for thread in threads:
        new_thread = EmailThread(
            id=thread["id"], title=thread["title"], source=thread["source"]
        )
        db.session.add(new_thread)
    db.session.commit()
    click.echo(DONE)


def import_email():
    click.echo("Importing Email...", nl=False)
    with open("./data/emails.json") as data_file:
        emails = json.load(data_file)

    for e in emails:
        satoshi_id = None
        if "satoshi_id" in e.keys():
            satoshi_id = e["satoshi_id"]
        parent = None
        if "parent" in e.keys():
            parent = Email.query.get(e["parent"])
        new_email = Email(
            id=e["id"],
            satoshi_id=satoshi_id,
            url=e["url"],
            subject=e["subject"],
            sent_from=e["sender"],
            date=parser.parse(e["date"]),
            text=e["text"],
            source=e["source"],
            source_id=e["source_id"],
            thread_id=e["thread_id"],
        )
        if parent:
            new_email.parent = parent
        db.session.add(new_email)
    db.session.commit()
    click.echo(DONE)


def import_forum_thread():
    click.echo("Importing ForumThread...", nl=False)
    with open("data/threads_forums.json") as data_file:
        threads = json.load(data_file)

    for thread in threads:
        new_thread = ForumThread(
            id=thread["id"],
            title=thread["title"],
            url=thread["url"],
            source=thread["source"],
        )
        db.session.add(new_thread)
    db.session.commit()
    click.echo(DONE)


def import_post():
    click.echo("Importing Post...", nl=False)
    with open("data/posts.json") as data_file:
        posts = json.load(data_file)

    for i, p in enumerate(posts, start=1):
        satoshi_id = None
        if "satoshi_id" in p.keys():
            satoshi_id = p["satoshi_id"]
        post = Post(
            id=i,
            satoshi_id=satoshi_id,
            url=p["url"],
            subject=p["subject"],
            poster_name=p["name"],
            poster_url=p["poster_url"],
            post_num=p["post_num"],
            is_displayed=p["is_displayed"],
            nested_level=p["nested_level"],
            date=parser.parse(p["date"]),
            text=p["content"],
            thread_id=p["thread_id"],
        )
        db.session.add(post)
    db.session.commit()
    click.echo(DONE)


def import_quote_category():
    click.echo("Importing QuoteCategory...", nl=False)
    with open("./data/quotecategories.json") as data_file:
        quotecategories = json.load(data_file)

    for qc in quotecategories:
        quote_category = QuoteCategory(slug=qc["slug"], name=qc["name"])
        db.session.add(quote_category)
    db.session.commit()
    click.echo(DONE)


def import_quote():
    click.echo("Importing Quote...", nl=False)
    with open("./data/quotes.json") as data_file:
        quotes = json.load(data_file)

    for i, quote in enumerate(quotes, start=1):
        q = Quote(
            id=i,
            text=quote["text"],
            date=parser.parse(quote["date"]).date(),
            medium=quote["medium"],
        )
        if "email_id" in quote:
            q.email_id = quote["email_id"]
        if "post_id" in quote:
            q.post_id = quote["post_id"]
        categories = []
        for cat in quote["category"].split(", "):
            categories += [get(QuoteCategory, slug=cat)]
        q.categories = categories
        db.session.add(q)
    db.session.commit()
    click.echo(DONE)


def import_author():
    click.echo("Importing Author...", nl=False)
    with open("./data/authors.json") as data_file:
        authors = json.load(data_file)

    for i, author in enumerate(authors, start=1):
        author = Author(
            id=i,
            first=author["first"],
            middle=author["middle"],
            last=author["last"],
            slug=author["slug"],
        )
        db.session.add(author)
    db.session.commit()
    click.echo(DONE)


def import_doc():
    click.echo("Importing Doc...", nl=False)
    with open("./data/literature.json") as data_file:
        docs = json.load(data_file)

    for doc in docs:
        authorlist = doc["author"]
        dbauthor = []
        for auth in authorlist:
            dbauthor += [get(Author, slug=auth)]
        formlist = doc["formats"]
        dbformat = []
        for form in formlist:
            dbformat += [get_or_create(Format, name=form)]
        catlist = doc["categories"]
        dbcat = []
        for cat in catlist:
            dbcat += [get_or_create(Category, name=cat)]
        if "external" in doc:
            ext = doc["external"]
        else:
            ext = None
        doc = Doc(
            id=doc["id"],
            title=doc["title"],
            author=dbauthor,
            date=doc["date"],
            slug=doc["slug"],
            formats=dbformat,
            categories=dbcat,
            doctype=doc["doctype"],
            external=ext,
        )
        db.session.add(doc)
    db.session.commit()
    click.echo(DONE)


def import_research_doc():
    click.echo("Importing ResearchDoc...", nl=False)
    with open("./data/research.json") as data_file:
        docs = json.load(data_file)

    for doc in docs:
        authorlist = doc["author"]
        dbauthor = []
        for auth in authorlist:
            dbauthor += [get(Author, slug=auth)]
        formlist = doc["formats"]
        dbformat = []
        for form in formlist:
            dbformat += [get_or_create(Format, name=form)]
        catlist = doc["categories"]
        dbcat = []
        for cat in catlist:
            dbcat += [get_or_create(Category, name=cat)]
        if "external" in doc:
            ext = doc["external"]
        else:
            ext = None
        if "lit_id" in doc:
            lit = doc["lit_id"]
        else:
            lit = None
        doc = ResearchDoc(
            id=doc["id"],
            title=doc["title"],
            author=dbauthor,
            date=doc["date"],
            slug=doc["slug"],
            formats=dbformat,
            categories=dbcat,
            doctype=doc["doctype"],
            external=ext,
            lit_id=lit,
        )
        db.session.add(doc)
    db.session.commit()
    click.echo(DONE)


def import_blog_series():
    click.echo("Importing BlogSeries...", nl=False)
    with open("./data/blogseries.json") as data_file:
        blogss = json.load(data_file)

    for i, blogs in enumerate(blogss, start=1):
        blog_series = BlogSeries(
            id=i,
            title=blogs["title"],
            slug=blogs["slug"],
            chapter_title=blogs["chapter_title"],
        )
        db.session.add(blog_series)
    db.session.commit()
    click.echo(DONE)


def import_blog_post():
    click.echo("Importing BlogPost...", nl=False)
    with open("./data/blogposts.json") as data_file:
        blogposts = json.load(data_file)

    for i, bp in enumerate(blogposts, start=1):
        blogpost = BlogPost(
            id=i,
            title=bp["title"],
            author=[get(Author, slug=bp["author"])],
            date=parser.parse(bp["date"]),
            added=parser.parse(bp["added"]),
            slug=bp["slug"],
            excerpt=bp["excerpt"],
        )
        db.session.add(blogpost)
        try:
            blogpost.series = get(BlogSeries, slug=bp["series"])
            blogpost.series_index = bp["series_index"]
        except KeyError:
            pass
        db.session.add(blogpost)
        for lang in bp["translations"]:
            translators = bp["translations"][lang]
            dbtranslator = []
            for translator in translators:
                dbtranslator += [get(Translator, name=translator)]
            blog_translation = BlogPostTranslation(
                language=get(Language, ietf=lang),
                translators=dbtranslator,
            )
            blogpost.translations.append(blog_translation)
        db.session.add(blogpost)
    db.session.commit()
    click.echo(DONE)


def import_skeptic():
    click.echo("Importing Skeptic...", nl=False)
    with open("./data/skeptics.json") as data_file:
        skeptics = json.load(data_file)

    for i, skeptic in enumerate(skeptics, start=1):
        slug_date = datetime.strftime(parser.parse(skeptic["date"]), "%Y-%m-%d")
        try:
            media_embed = skeptic["media_embed"]
        except KeyError:
            media_embed = ""
        try:
            twitter_screenshot = skeptic["twitter_screenshot"]
        except KeyError:
            twitter_screenshot = False
        skeptic = Skeptic(
            id=i,
            name=skeptic["name"],
            title=skeptic["title"],
            article=skeptic["article"],
            date=parser.parse(skeptic["date"]),
            source=skeptic["source"],
            excerpt=skeptic["excerpt"],
            price=skeptic["price"],
            link=skeptic["link"],
            waybacklink=skeptic["waybacklink"],
            media_embed=media_embed,
            twitter_screenshot=twitter_screenshot,
            slug="{}-{}".format(skeptic["slug"], slug_date),
        )
        db.session.add(skeptic)
    db.session.commit()
    click.echo(DONE)
    update_skeptics()


def import_episode():
    click.echo("Importing Episode...", nl=False)
    with open("./data/episodes.json") as data_file:
        episodes = json.load(data_file)

    for ep in episodes:
        episode = Episode(
            id=ep["id"],
            title=ep["title"],
            date=parser.parse(ep["date"]),
            duration=ep["duration"],
            subtitle=ep["subtitle"],
            summary=ep["summary"],
            slug=ep["slug"],
            youtube=ep["youtube"],
            time=parser.parse(ep["time"]),
        )
        db.session.add(episode)
    db.session.commit()
    click.echo(DONE)


@bp.cli.command()
def seed():
    """Initialize and seed database."""
    export_prices()
    flush_db()
    import_language()
    import_translator()
    import_email_thread()
    import_email()
    import_forum_thread()
    import_post()
    import_quote_category()
    import_quote()
    import_author()
    import_doc()
    import_research_doc()
    import_blog_series()
    import_blog_post()
    import_prices()
    import_skeptic()
    import_episode()
    click.echo(color_text("Finished importing data!"))
