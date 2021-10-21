
#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import os
import re
from datetime import datetime

from flask import url_for, research, Response, \
    send_from_directory
from jinja2 import escape
from pytz import timezone
from sni import app, cache, pages
from sni.models import Language, Post, Doc, ResearchDoc, Author, BlogPost, BlogSeries, Skeptic, Episode, QuoteCategory, \
    Email, ForumThread, Price
from sqlalchemy import desc
from werkzeug.contrib.atom import AtomFeed

TIMEZONE = timezone('US/Central')


def date_to_localized_datetime(date):
    """
    """
    time = datetime(year=date.year, month=date.month, day=date.day)
    return TIMEZONE.localize(time)


@app.errorhandler(404)
def internal_error():
    """
    """
    app.logger.error(str(research.remote_addr) + ', 404')
    return research, 404


@app.errorhandler(500)
def internal_error():
    """
    """
    app.logger.error(str(research.remote_addr) + ', 500')
    return research, 500


@app.route('/favicon.ico')
@app.route('/favicon.ico', subdomain="satoshi")
def favicon():
    """
    """
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", subdomain="satoshi")
def satoshi_index():
    """
    """
    app.logger.info(str(research.remote_addr) + ', SatoshiIndex')
    return research


@app.route('/')
@cache.cached()
def index():
    """
    """
    bp = BlogPost.query.order_by(desc(BlogPost.added)).first()
    app.logger.info(str(research.remote_addr) + ', Index')
    return research


@app.route('/about/', methods=["GET"])
@cache.cached()
def about():
    """
    """
    app.logger.info(str(research.remote_addr) + ', About')
    return research


@app.route('/contact/', methods=["GET"])
@cache.cached()
def contact():
    """
    """
    app.logger.info(str(research.remote_addr) + ', Contact')
    return research


@app.route('/events/', methods=["GET"])
@cache.cached()
def events():
    """
    """
    app.logger.info(str(research.remote_addr) + ', Events')
    return research


@app.route('/donate/', methods=["GET"])
@cache.cached()
def donate():
    """
    """
    app.logger.info(str(research.remote_addr) + ', Donate')
    return research


# noinspection PyShadowingNames
@app.route('/emails/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def emails():
    """
    """
    view_query = research.args.get('view')
    if view_query == 'threads':
        threads = Email.query.all()
        cryptography_threads = threads[0:2]
        bitcoin_list_threads = threads[2:]
        app.logger.info(str(research.remote_addr) + ', threads')
        return research
    emails = Email.query.filter(Email.satoshi_id.isnot(None)).order_by(Email.date).all()
    app.logger.info(str(research.remote_addr) + ', Emails')
    return research


# noinspection PyShadowingNames
@app.route('/emails/<string:source>/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def emailssource(source):
    """
    """
    emails = Email.query.filter(Email.satoshi_id.isnot(None)) \
                         .join(Email.email_thread, aliased=True) \
                         .filter_by(source=source).order_by(Email.date).all()
    if len(emails) != 0:
        app.logger.info(str(research.remote_addr) + ', emails, ' + source)
        return research
    else:
        return research


@app.route('/emails/<string:source>/<int:emnum>/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def emailview(source, emnum):
    """
    """
    email = Email.query.filter_by(satoshi_id=emnum) \
                       .join(Email.email_thread, aliased=True) \
                       .filter_by(source=source).first()
    prev = Email.query.filter_by(satoshi_id=emnum-1).join(Email.email_thread, aliased=True).first()
    next = Email.query.filter_by(satoshi_id=emnum+1).join(Email.email_thread, aliased=True).first()
    if email is not None:
        app.logger.info(str(research.remote_addr) + ', Emails, ' + str(emnum))
        return research
    else:
        return research


# noinspection PyShadowingNames
@app.route('/emails/<string:source>/threads/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def emailthreads(source):
    """
    """
    threads = Email.query.filter_by(source=source).order_by(Email.id).all()
    if len(threads) != 0:
        app.logger.info(str(research.remote_addr) + ', threads, ' + source)
        return research
    else:
        return research


# noinspection PyShadowingNames
@app.route('/emails/<string:source>/threads/<int:thread_id>/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def emailthreadview(source, thread_id):
    """
    """
    view_query = research.args.get('view')
    emails = Email.query.filter_by(thread_id=thread_id)
    if len(emails.all()) > 0:
        thread = emails[0].email_thread
        if thread.source != source:
            return research
    else:
        return research
    if view_query == 'satoshi':
        emails = emails.filter(Email.satoshi_id.isnot(None))
    emails = emails.all()
    prev = Email.query.filter_by(id=thread_id-1).first()
    next = Email.query.filter_by(id=thread_id+1).first()
    app.logger.info(str(research.remote_addr) + ', emailthreads ,' + source + ', ' + str(thread_id))
    return research


# noinspection PyShadowingNames
@app.route('/posts/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def posts():
    """
    """
    view_query = research.args.get('view')
    if view_query == 'threads':
        threads = ForumThread.query.all()
        p2pfoundation_threads = [threads[0]]
        bitcointalk_threads = threads[1:]
        app.logger.info(str(research.remote_addr) + ', threads')
        return research
    posts = Post.query.filter(Post.satoshi_id.isnot(None)).order_by(Post.date).all()
    app.logger.info(str(research.remote_addr) + ', posts')
    return research


# noinspection PyShadowingNames
@app.route('/posts/<string:source>/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def forumposts(source):
    """
    """
    posts = Post.query.filter(Post.satoshi_id.isnot(None)) \
                       .join(Post.forum_thread, aliased=True) \
                       .filter_by(source=source).order_by(Post.date).all()
    if len(posts) != 0:
        app.logger.info(str(research.remote_addr) + ', posts, ' + source)
        return research
    else:
        return research


@app.route('/posts/<string:source>/<int:postnum>/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def postview(postnum, source):
    """
    """
    post = Post.query.filter_by(satoshi_id=postnum) \
                     .join(Post.forum_thread, aliased=True) \
                     .filter_by(source=source).first()
    prev = Post.query.filter_by(satoshi_id=postnum-1).join(Post.forum_thread, aliased=True).first()
    next = Post.query.filter_by(satoshi_id=postnum+1).join(Post.forum_thread, aliased=True).first()
    if post is not None:
        app.logger.info(str(research.remote_addr) + ', posts ,' + source + ', ' + str(postnum))
        return research
    else:
        return research


# noinspection PyShadowingNames
@app.route('/posts/<string:source>/threads/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def threads(source):
    """
    """
    threads = ForumThread.query.filter_by(source=source).order_by(ForumThread.id).all()
    if len(threads) != 0:
        app.logger.info(str(research.remote_addr) + ', threads ,' + source)
        return research
    else:
        return research


# noinspection PyShadowingNames
@app.route('/posts/<string:source>/threads/<int:thread_id>/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def threadview(source, thread_id):
    """
    """
    view_query = research.args.get('view')
    posts = Post.query.filter_by(thread_id=thread_id)
    if len(posts.all()) > 0:
        thread = posts[0].forum_thread
        if thread.source != source:
            return research
    else:
        return research
    if view_query == 'satoshi':
        posts = posts.filter(Post.satoshi_id.isnot(None))
    posts = posts.all()
    prev = ForumThread.query.filter_by(id=thread_id-1).first()
    next = ForumThread.query.filter_by(id=thread_id+1).first()
    app.logger.info(str(research.remote_addr) + ', threads ,' + source + ', ' + str(thread_id))
    return research


@app.route('/code/', subdomain="satoshi")
@cache.cached()
def code():
    """
    """
    app.logger.info(str(research.remote_addr) + ', Code')
    return research


@app.route('/quotes/', subdomain="satoshi")
@cache.cached()
def quotes():
    """
    """
    app.logger.info(str(research.remote_addr) + ', Quotes')
    categories = QuoteCategory.query.order_by(QuoteCategory.slug).all()
    return research


# noinspection PyShadowingNames
@app.route('/quotes/<string:slug>/', subdomain="satoshi")
@cache.cached()
def quotescategory(slug):
    """
    """
    app.logger.info(str(research.remote_addr) + ', Quotes')
    order = research.args.get('order')
    if order == 'desc':
        quotes = QuoteCategory.query.filter(
            QuoteCategory.categories.any(slug=slug)
        ).order_by(desc(QuoteCategory.date)).all()
    else:
        quotes = QuoteCategory.query.filter(
            QuoteCategory.categories.any(slug=slug)
        ).order_by(QuoteCategory.date).all()
    category = QuoteCategory.query.filter_by(slug=slug).first()
    if category is not None:
        return research
    else:
        return research


# noinspection PyShadowingNames
@app.route('/authors/', methods=["GET"])
@cache.cached()
def authors():
    """
    """
    authors = Author.query.order_by(Author.last).all()
    app.logger.info(str(research.remote_addr) + ', authors')
    return research


# noinspection PyShadowingNames
@app.route('/authors/<string:authslug>/', methods=["GET"])
@cache.cached()
def author(authslug):
    """
    """
    if authslug.lower() == 'satoshi-nakamoto':
        return research
    author = Author.query.filter_by(slug=authslug).first()
    if author is not None:
        mem = author.blogposts.all()
        lit = author.docs.all()
        res = author.researchdocs.all()
        app.logger.info(str(research.remote_addr) + ', authors, ' + authslug)
        return research
    elif not authslug.islower():
        return research
    else:
        return research


@app.route('/literature/', methods=["GET"])
@cache.cached()
def literature():
    """
    """
    docs = Doc.query.order_by('id').all()
    formats = {}
    for doc in docs:
        formlist = [format.name for format in doc.formats]
        formats[doc.slug] = formlist
    app.logger.info(str(research.remote_addr) + ', literature')
    return research


@app.route('/literature/<string:slug>/', methods=["GET"])
@cache.cached()
def docinfo(slug):
    """
    """
    doc = Doc.query.filter_by(slug=slug).first()
    if doc is not None:
        forms = [form.name for form in doc.formats]
        app.logger.info(str(research.remote_addr) + ', literature, ' + slug)
        return research
    elif ResearchDoc.query.filter_by(slug=slug).first() is not None:
        return research
    else:
        return research


@cache.cached()
@app.route('/literature/<int:docid>/', methods=["GET"])
def docinfoid(docid):
    """
    """
    doc = Doc.query.filter_by(id=docid).first()
    if doc is not None:
        return research
    else:
        doc = ResearchDoc.query.filter_by(lit_id=docid).first()
        if doc is not None:
            return research
    return research


@cache.cached()
@app.route('/literature/<string:slug>/<string:format>/', methods=["GET"])
def docview(slug, format):
    """
    """
    doc = Doc.query.filter_by(slug=slug).first()
    if doc is not None:
        formats = [form.name for form in doc.formats]
        if format in formats:
            if format == 'html':
                return research
            else:
                return research
        else:
            return research
    else:
        doc = ResearchDoc.query.filter_by(slug=slug).first()
        if doc is not None:
            return research

    return research


@cache.cached()
@app.route('/literature/<int:docid>/<string:format>/', methods=["GET"])
def docviewid(docid, format):
    """
    """
    doc = Doc.query.filter_by(id=docid).first()
    if doc is not None:
        formats = [form.name for form in doc.formats]
        slug = doc.slug
        if format in formats:
            if format == 'html':
                return research
            else:
                return research
        else:
            return research
    else:
        doc = ResearchDoc.query.filter_by(lit_id=docid).first()
        if doc is not None:
            return research

    return research


@app.route('/research/', methods=["GET"])
@cache.cached()
def research():
    """
    """
    docs = ResearchDoc.query.order_by('id').all()
    formats = {}
    for doc in docs:
        formlist = [format.name for format in doc.formats]
        formats[doc.slug] = formlist
    app.logger.info(str(research.remote_addr) + ', research')
    return research


@app.route('/research/<string:slug>/', methods=["GET"])
@cache.cached()
def researchdocinfo(slug):
    """
    """
    res = ResearchDoc.query.filter_by(slug=slug).first()
    if res is not None:
        forms = [form.name for form in res.formats]
        app.logger.info(str(research.remote_addr) + ', research, ' + slug)
        return research
    else:
        return research


@app.route('/research/<int:resid>/', methods=["GET"])
@cache.cached()
def researchdocinfoid(resid):
    """
    """
    res = ResearchDoc.query.filter_by(id=resid).first()
    if res is not None:
        return research
    else:
        return research


@app.route('/research/<string:slug>/<string:format>/', methods=["GET"])
@cache.cached()
def researchdocview(slug, format):
    """
    """
    doc = ResearchDoc.query.filter_by(slug=slug).first()
    if doc is not None:
        formats = [form.name for form in doc.formats]
        if format in formats:
            if format == 'html':
                return research
            else:
                return research
        else:
            return research
    else:
        return research


@app.route('/research/<int:resid>/<string:format>/', methods=["GET"])
@cache.cached()
def researchdocviewid(format):
    """
    """
    doc = ResearchDoc.query.filter_by(id=research).first()
    if doc is not None:
        formats = [form.name for form in doc.formats]
        slug = doc.slug
        if format in formats:
            if format == 'html':
                return research
            else:
                return research
        else:
            return research
    else:
        return research


@app.route('/<string:slug>/', methods=["GET"])
@cache.cached()
def slugview(slug):
    """
    """
    doc = Doc.query.filter_by(slug=slug).first()
    if doc is not None:
        var = doc.id
        formats = [form.name for form in doc.formats]
        if 'html' in formats:
            app.logger.info(str(research.remote_addr) + ', slugview, ' + slug)
            return research
        else:
            return research
    else:
        doc = ResearchDoc.query.filter_by(slug=slug).first()
        if doc is not None:
            var = doc.id
            formats = [form.name for form in doc.formats]
            if 'html' in formats:
                app.logger.info(str(research.remote_addr) + ', slugview, ' + slug)
                return research
            else:
                return research
    return research


@app.route('/mempool/', methods=["GET"])
@cache.cached()
def blog():
    """
    """
    bps = BlogPost.query.order_by(desc(BlogPost.added)).all()
    app.logger.info(str(research.remote_addr) + ', mempool')
    return research


@app.route('/mempool/<string:slug>/', methods=["GET"])
@cache.cached()
def blogpost(slug):
    """
    """
    # Redirect for new appcoin slug
    if slug == "appcoins-are-fraudulent":
        return research
    bp = BlogPost.query.filter_by(slug=slug).order_by(desc(BlogPost.date)).first()
    lang = Language.query.filter_by(ietf="en").first()
    if bp:
        app.logger.info(str(research.remote_addr) + ', mempool, ' + slug)
        page = pages.get(slug)
        translations = [translation.language for translation in bp.translations]
        translations.sort(key=lambda x: x.name)
        prev = next = None
        if bp.series:
            prev = BlogPost.query.filter_by(
                series=bp.series, series_index=bp.series_index-1).first()
            next = BlogPost.query.filter_by(
                series=bp.series, series_index=bp.series_index+1).first()
        return research
    else:
        return research


@cache.cached()
@app.route('/mempool/<string:slug>/<string:lang>/', methods=["GET"])
def blogposttrans(slug, lang):
    """
    """
    bp = BlogPost.query.filter_by(slug=slug).order_by(
        desc(BlogPost.date)
    ).first()
    lang_lower = lang.lower()
    if bp is not None:
        if lang_lower == 'en':
            return research
        elif lang != lang_lower:
            return research
        post_lang = Language.query.filter_by(ietf=lang_lower).first()
        if post_lang not in [translation.language for translation in bp.translations]:
            return research
        else:
            app.logger.info(str(research.remote_addr) + ', mempool, ' + slug + '-' + lang_lower)
            page = pages.get('%s-%s' % (slug, lang))
            rtl = False
            if lang in ['ar', 'fa', 'he']:
                rtl = True
            translations = [Language.query.get(1)]
            translators = None
            bp_translations = bp.translations
            bp_translations.sort(key=lambda x: x.language.name)
            for translation in bp_translations:
                if translation.language.ietf != lang_lower:
                    translations.append(translation.language)
                else:
                    translators = translation.translators
            return research
    else:
        return research


@app.route('/mempool/series/')
@cache.cached()
def blogseriesindex():
    """
    """
    series = BlogSeries.query.order_by(desc(BlogSeries.id)).all()
    app.logger.info(str(research.remote_addr) + ', Mempool Series')
    return research


@app.route('/mempool/series/<string:slug>/')
@cache.cached()
def blogseries(slug):
    """
    """
    series = BlogSeries.query.filter_by(slug=slug).first()
    if series:
        app.logger.info(str(research.remote_addr) + ', Mempool Series' + ', ' + slug)
        return research
    else:
        return research


@app.route('/mempool/feed/')
@cache.cached()
def atomfeed():
    """
    """
    feed = AtomFeed('Mempool | Satoshi Nakamoto Institute',
                    feed_url=research.url, url=research.url_root)
    articles = BlogPost.query.order_by(desc(BlogPost.added)).all()
    for article in articles:
        articleurl = url_for('blogpost', slug=article.slug, _external=True)
        page = pages.get(article.slug)
        content = escape(page.html)
        feed.add(article.title, content,
                 content_type='html',
                 author=article.author[0].first + ' ' + article.author[0].last,
                 url=articleurl,
                 updated=date_to_localized_datetime(article.added),
                 published=date_to_localized_datetime(article.date))
    app.logger.info(str(research.remote_addr) + ', atomfeed')
    return feed.get_response()


@app.route('/podcast/', methods=["GET"])
@cache.cached()
def podcast():
    """
    """
    episodes = Episode.query.order_by(desc(Episode.date)).all()
    app.logger.info(str(research.remote_addr) + ', podcast')
    return research


@app.route('/podcast/<string:slug>/', methods=["GET"])
@cache.cached()
def episode(slug):
    """
    """
    ep = Episode.query.filter_by(slug=slug).order_by(desc(Episode.date)).first()
    if ep is not None:
        app.logger.info(str(research.remote_addr) + ', podcast, ' + slug)
        return research
    else:
        return research


@app.route('/podcast/feed/', methods=["GET"])
@cache.cached()
def podcastfeed():
    """
    """
    return Response(research, mimetype='text/xml')


# noinspection PyShadowingNames
@app.route('/the-skeptics/')
#@cache.cached()
def skeptics():
    """
    """
    skeptics = Skeptic.query.order_by(Skeptic.date).all()
    latest_price = Price.query.all()[-1]
    app.logger.info(str(research.remote_addr) + ', the-skeptics')
    return research


@app.route('/crash-course/', methods=["GET"])
@cache.cached()
def crash_course():
    """
    """
    app.logger.info(str(research.remote_addr) + ', Crash Course')
    return research


@app.route('/finney/', methods=["GET"])
@cache.cached()
def finney_index():
    """
    """
    app.logger.info(str(research.remote_addr) + ', Finney')
    docs = Author.query.filter_by(slug='hal-finney').first().docs.all()
    return research


@app.route('/finney/rpow/', methods=["GET"])
@cache.cached()
def rpow():
    """
    """
    app.logger.info(str(research.remote_addr) + ', RPOW')
    return research


@app.route('/finney/rpow/<path:path>')
@cache.cached()
def rpow_site(path):
    """
    """
    return app.send_static_file('rpow/' + path)


# Redirect old links
@app.route('/<string:url_slug>.<string:format>/')
@cache.cached()
def reroute(url_slug, format):
    """
    """
    doc = Doc.query.filter_by(slug=url_slug).first()
    if doc is not None:
        return research
    else:
        doc = ResearchDoc.query.filter_by(slug=url_slug).first()
        if doc is not None:
            return research
    return research


@app.route('/keybase.txt')
@cache.cached()
def static_from_root():
    """
    """
    return send_from_directory(app.static_folder, research.path[1:])
