#!/usr/bin/env python
#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import json
import datetime
import csv
from dateutil import parser
from datetime import datetime

from sni import db
from sni.models import *

import click


def color_text(text, color='green'):
    return click.style(text, fg=color)


DONE = color_text('Done!')


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
    click.echo('Iniitalizing database...', nl=False)
    db.drop_all()
    db.create_all()
    click.echo(DONE)


def import_language():
    click.echo('Importing Language...', nl=False)
    with open('data/languages.json') as data_file:
        languages = json.load(data_file)

    for language in languages:
        new_language = Language(
            name=language['name'],
            ietf=language['ietf']
        )
        db.session.add(new_language)
        db.session.commit()
    click.echo(DONE)


def import_email_thread():
    click.echo('Importing EmailThread...', nl=False)
    with open('data/threads_emails.json') as data_file:
        threads = json.load(data_file)

    for thread in threads:
        new_thread = EmailThread(
            id=thread['id'],
            title=thread['title'],
            source=thread['source']
        )
        db.session.add(new_thread)
        db.session.commit()
    click.echo(DONE)


def import_email():
    click.echo('Importing Email...', nl=False)
    with open('./data/emails.json') as data_file:
        emails = json.load(data_file)

    for e in emails:
        satoshi_id = None
        if 'satoshi_id' in e.keys():
            satoshi_id = e['satoshi_id']
        parent = None
        if 'parent' in e.keys():
            parent = Email.query.get(e['parent'])
        new_email = Email(
            id=e['id'],
            satoshi_id=satoshi_id,
            url=e['url'],
            subject=e['subject'],
            sent_from=e['sender'],
            date=parser.parse(e['date']),
            text=e['text'],
            source=e['source'],
            source_id=e['source_id'],
            thread_id=e['thread_id'])
        if parent:
            new_email.parent = parent
        db.session.add(new_email)
        db.session.commit()
    click.echo(DONE)


def import_forum_thread():
    click.echo('Importing ForumThread...', nl=False)
    with open('data/threads_forums.json') as data_file:
        threads = json.load(data_file)

    for thread in threads:
        new_thread = ForumThread(
            id=thread['id'],
            title=thread['title'],
            url=thread['url'],
            source=thread['source']
        )
        db.session.add(new_thread)
        db.session.commit()
    click.echo(DONE)


def import_post():
    click.echo('Importing Post...', nl=False)
    with open('data/posts.json') as data_file:
        posts = json.load(data_file)

    for i, p in enumerate(posts, start=1):
        satoshi_id = None
        if 'satoshi_id' in p.keys():
            satoshi_id = p['satoshi_id']
        post = Post(
            id=i,
            satoshi_id=satoshi_id,
            url=p['url'],
            subject=p['subject'],
            poster_name=p['name'],
            poster_url=p['poster_url'],
            post_num=p['post_num'],
            is_displayed=p['is_displayed'],
            nested_level=p['nested_level'],
            date=parser.parse(p['date']),
            text=p['content'],
            thread_id=p['thread_id']
        )
        db.session.add(post)
        db.session.commit()
    click.echo(DONE)


def import_quote_category():
    click.echo('Importing QuoteCategory...', nl=False)
    with open('./data/quotecategories.json') as data_file:
        quotecategories = json.load(data_file)

    for qc in quotecategories:
        quote_category = QuoteCategory(
            slug=qc['slug'],
            name=qc['name']
        )
        db.session.add(quote_category)
        db.session.commit()
    click.echo(DONE)


def import_quote():
    click.echo('Importing Quote...', nl=False)
    with open('./data/quotes.json') as data_file:
        quotes = json.load(data_file)

    for i, quote in enumerate(quotes, start=1):
        q = Quote(
            id=i,
            text=quote['text'],
            date=parser.parse(quote['date']).date(),
            medium=quote['medium']
        )
        if 'email_id' in quote:
            q.email_id = quote['email_id']
        if 'post_id' in quote:
            q.post_id = quote['post_id']
        categories = []
        for cat in quote['category'].split(', '):
            categories += [get(QuoteCategory, slug=cat)]
        q.categories = categories
        db.session.add(q)
        db.session.commit()
    click.echo(DONE)


def import_author():
    click.echo('Importing Author...', nl=False)
    with open('./data/authors.json') as data_file:
        authors = json.load(data_file)

    for i, author in enumerate(authors, start=1):
        author = Author(
            id=i,
            first=author['first'],
            middle=author['middle'],
            last=author['last'],
            slug=author['slug'])
        db.session.add(author)
        db.session.commit()
    click.echo(DONE)


def import_doc():
    click.echo('Importing Doc...', nl=False)
    with open('./data/literature.json') as data_file:
        docs = json.load(data_file)

    for doc in docs:
        authorlist = doc['author']
        dbauthor = []
        for auth in authorlist:
            dbauthor += [get(Author, slug=auth)]
        formlist = doc['formats']
        dbformat = []
        for form in formlist:
            dbformat += [get_or_create(Format, name=form)]
        catlist = doc['categories']
        dbcat = []
        for cat in catlist:
            dbcat += [get_or_create(Category, name=cat)]
        if 'external' in doc:
            ext = doc['external']
        else:
            ext = None
        doc = Doc(
            id=doc['id'],
            title=doc['title'],
            author=dbauthor,
            date=doc['date'],
            slug=doc['slug'],
            formats=dbformat,
            categories=dbcat,
            doctype=doc['doctype'],
            external=ext)
        db.session.add(doc)
        db.session.commit()
    click.echo(DONE)


def import_research_doc():
    click.echo('Importing ResearchDoc...', nl=False)
    with open('./data/research.json') as data_file:
        docs = json.load(data_file)

    for doc in docs:
        authorlist = doc['author']
        dbauthor = []
        for auth in authorlist:
            dbauthor += [get(Author, slug=auth)]
        formlist = doc['formats']
        dbformat = []
        for form in formlist:
            dbformat += [get_or_create(Format, name=form)]
        catlist = doc['categories']
        dbcat = []
        for cat in catlist:
            dbcat += [get_or_create(Category, name=cat)]
        if 'external' in doc:
            ext = doc['external']
        else:
            ext = None
        if 'lit_id' in doc:
            lit = doc['lit_id']
        else:
            lit_id = None
        doc = ResearchDoc(
            id=doc['id'],
            title=doc['title'],
            author=dbauthor,
            date=doc['date'],
            slug=doc['slug'],
            formats=dbformat,
            categories=dbcat,
            doctype=doc['doctype'],
            external=ext,
            lit_id=lit)
        db.session.add(doc)
        db.session.commit()
    click.echo(DONE)


def import_blog_series():
    click.echo('Importing BlogSeries...', nl=False)
    with open('./data/blogseries.json') as data_file:
        blogss = json.load(data_file)

    for i, blogs in enumerate(blogss, start=1):
        blog_series = BlogSeries(
            id=i,
            title=blogs['title'],
            slug=blogs['slug'],
        )
        db.session.add(blog_series)
        db.session.commit()
    click.echo(DONE)


def import_blog_post():
    click.echo('Importing BlogPost...', nl=False)
    with open('./data/blogposts.json') as data_file:
        blogposts = json.load(data_file)

    for i, bp in enumerate(blogposts, start=1):
        blogpost = BlogPost(
            id=i,
            title=bp['title'],
            author=[get(Author, slug=bp['author'])],
            date=parser.parse(bp['date']),
            added=parser.parse(bp['added']),
            slug=bp['slug'],
            excerpt=bp['excerpt'],
            languages=bp['languages'])
        try:
            blogpost.series = get(BlogSeries, slug=bp['series'])
            blogpost.series_index = bp['series_index']
        except KeyError:
            pass
        db.session.add(blogpost)
        db.session.commit()
    click.echo(DONE)


def import_skeptic():
    click.echo('Importing Skeptic...', nl=False)
    with open('./data/skeptics.json') as data_file:
        skeptics = json.load(data_file)

    for i, skeptic in enumerate(skeptics, start=1):
        slug_date = datetime.strftime(parser.parse(skeptic['date']), '%Y-%m-%d')
        try:
            twitter_embed = skeptic['twitter_embed']
        except KeyError:
            twitter_embed = ''
        try:
            twitter_screenshot = skeptic['twitter_screenshot']
        except KeyError:
            twitter_screenshot = False
        skeptic = Skeptic(
            id=i,
            name=skeptic['name'],
            title=skeptic['title'],
            article=skeptic['article'],
            date=parser.parse(skeptic['date']),
            source=skeptic['source'],
            excerpt=skeptic['excerpt'],
            price=skeptic['price'],
            link=skeptic['link'],
            waybacklink=skeptic['waybacklink'],
            twitter_embed=twitter_embed,
            twitter_screenshot=twitter_screenshot,
            slug='{}-{}'.format(skeptic['slug'], slug_date)
        )
        db.session.add(skeptic)
        db.session.commit()
    click.echo(DONE)


def import_episode():
    click.echo('Importing Episode...', nl=False)
    with open('./data/episodes.json') as data_file:
        episodes = json.load(data_file)

    for ep in episodes:
        episode = Episode(
            id=ep['id'],
            title=ep['title'],
            date=parser.parse(ep['date']),
            duration=ep['duration'],
            subtitle=ep['subtitle'],
            summary=ep['summary'],
            slug=ep['slug'],
            youtube=ep['youtube'],
            address=ep['address'],
            time=parser.parse(ep['time']))
        db.session.add(episode)
        db.session.commit()
    click.echo(DONE)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--content/--no-content', default=False,
              help='Update literature and mempool related tables')
@click.option('--skeptic/--no-skeptic', default=False,
              help='Update skeptic related tables')
def update(content, skeptic):
    """Script to initialize and/or update database."""
    if content:
        click.echo('Deleting Language...', nl=False)
        langs = Language.query.all()
        for lang in langs:
            db.session.delete(lang)
        db.session.commit()
        click.echo('Deleting Category...', nl=False)
        cats = Category.query.all()
        for cat in cats:
            db.session.delete(cat)
        db.session.commit()
        click.echo(DONE)
        click.echo('Deleting Format...', nl=False)
        forms = Format.query.all()
        for form in forms:
            db.session.delete(form)
        db.session.commit()
        click.echo(DONE)
        click.echo('Deleting Author...', nl=False)
        auths = Author.query.all()
        for auth in auths:
            db.session.delete(auth)
        db.session.commit()
        click.echo(DONE)
        import_author()
        click.echo('Deleting Doc...', nl=False)
        Doc.query.delete()
        click.echo(DONE)
        click.echo('Deleting ResearchDoc...', nl=False)
        ResearchDoc.query.delete()
        click.echo(DONE)
        import_doc()
        import_research_doc()
        click.echo('Deleting BlogPost...', nl=False)
        BlogPost.query.delete()
        click.echo(DONE)
        click.echo('Deleting BlogSeries...', nl=False)
        BlogSeries.query.delete()
        click.echo(DONE)
        import_blog_series()
        import_blog_post()
    if skeptic:
        click.echo('Deleting Skeptic...', nl=False)
        Skeptic.query.delete()
        click.echo(DONE)
        import_skeptic()
    if not content and not skeptic:
        flush_db()
        import_language()
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
        import_skeptic()
        import_episode()
    click.echo(color_text('Finished importing data!'))


if __name__ == '__main__':
    cli()
