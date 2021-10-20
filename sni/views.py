
#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import os
import re
from datetime import datetime

from flask import url_for, re, Response, \
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
    app.logger.error(str(re.remote_addr) + ', 404')
    return re('404.html'), 404


@app.errorhandler(500)
def internal_error():
    """
    """
    app.logger.error(str(re.remote_addr) + ', 500')
    return re('500.html'), 500


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
    app.logger.info(str(re.remote_addr) + ', SatoshiIndex')
    return re("satoshiindex.html")


@app.route('/')
@cache.cached()
def index():
    """
    """
    bp = BlogPost.query.order_by(desc(BlogPost.added)).first()
    app.logger.info(str(re.remote_addr) + ', Index')
    return re("index.html", bp=bp)


@app.route('/about/', methods=["GET"])
@cache.cached()
def about():
    """
    """
    app.logger.info(str(re.remote_addr) + ', About')
    return re("about.html")


@app.route('/contact/', methods=["GET"])
@cache.cached()
def contact():
    """
    """
    app.logger.info(str(re.remote_addr) + ', Contact')
    return re("contact.html")


@app.route('/events/', methods=["GET"])
@cache.cached()
def events():
    """
    """
    app.logger.info(str(re.remote_addr) + ', Events')
    return re("events.html")


@app.route('/donate/', methods=["GET"])
@cache.cached()
def donate():
    """
    """
    app.logger.info(str(re.remote_addr) + ', Donate')
    return re("donate.html")


# noinspection PyShadowingNames
@app.route('/emails/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def emails():
    """
    """
    view_query = re.args.get('view')
    if view_query == 'threads':
        threads = Email.query.all()
        cryptography_threads = threads[0:2]
        bitcoin_list_threads = threads[2:]
        app.logger.info(str(re.remote_addr) + ', threads')
        return re(
            "threads_emails.html", threads=threads, cryptography_threads=cryptography_threads,
            bitcoin_list_threads=bitcoin_list_threads, source=None)
    emails = Email.query.filter(Email.satoshi_id.isnot(None)).order_by(Email.date).all()
    app.logger.info(str(re.remote_addr) + ', Emails')
    return re("emails.html", emails=emails)


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
        app.logger.info(str(re.remote_addr) + ', emails, ' + source)
        return re("emails.html", emails=emails, source=source)
    else:
        return re(url_for('emails'))


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
        app.logger.info(str(re.remote_addr) + ', Emails, ' + str(emnum))
        return re("emailview.html", email=email, prev=prev, next=next)
    else:
        return re('emails')


# noinspection PyShadowingNames
@app.route('/emails/<string:source>/threads/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def emailthreads(source):
    """
    """
    threads = Email.query.filter_by(source=source).order_by(Email.id).all()
    if len(threads) != 0:
        app.logger.info(str(re.remote_addr) + ', threads, ' + source)
        return re("threads_emails.html", threads=threads, source=source)
    else:
        return re(url_for('emails', view='threads'))


# noinspection PyShadowingNames
@app.route('/emails/<string:source>/threads/<int:thread_id>/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def emailthreadview(source, thread_id):
    """
    """
    view_query = re.args.get('view')
    emails = Email.query.filter_by(thread_id=thread_id)
    if len(emails.all()) > 0:
        thread = emails[0].email_thread
        if thread.source != source:
            return re(url_for('emailthreadview', source=thread.source, thread_id=thread_id))
    else:
        return re(url_for('emails', view='threads'))
    if view_query == 'satoshi':
        emails = emails.filter(Email.satoshi_id.isnot(None))
    emails = emails.all()
    prev = Email.query.filter_by(id=thread_id-1).first()
    next = Email.query.filter_by(id=thread_id+1).first()
    app.logger.info(str(re.remote_addr) + ', emailthreads ,' + source + ', ' + str(thread_id))
    return re("threadview_emails.html", emails=emails, prev=prev, next=next)


# noinspection PyShadowingNames
@app.route('/posts/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def posts():
    """
    """
    view_query = re.args.get('view')
    if view_query == 'threads':
        threads = ForumThread.query.all()
        p2pfoundation_threads = [threads[0]]
        bitcointalk_threads = threads[1:]
        app.logger.info(str(re.remote_addr) + ', threads')
        return re(
            "threads.html", threads=threads, p2pfoundation_threads=p2pfoundation_threads,
            bitcointalk_threads=bitcointalk_threads, source=None)
    posts = Post.query.filter(Post.satoshi_id.isnot(None)).order_by(Post.date).all()
    app.logger.info(str(re.remote_addr) + ', posts')
    return re("posts.html", posts=posts, source=None)


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
        app.logger.info(str(re.remote_addr) + ', posts, ' + source)
        return re("posts.html", posts=posts, source=source)
    else:
        return re(url_for('posts'))


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
        app.logger.info(str(re.remote_addr) + ', posts ,' + source + ', ' + str(postnum))
        return re("postview.html", post=post, prev=prev,
                               next=next)
    else:
        return re('posts')


# noinspection PyShadowingNames
@app.route('/posts/<string:source>/threads/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def threads(source):
    """
    """
    threads = ForumThread.query.filter_by(source=source).order_by(ForumThread.id).all()
    if len(threads) != 0:
        app.logger.info(str(re.remote_addr) + ', threads ,' + source)
        return re("threads.html", threads=threads, source=source)
    else:
        return re(url_for('posts', view='threads'))


# noinspection PyShadowingNames
@app.route('/posts/<string:source>/threads/<int:thread_id>/', subdomain="satoshi", methods=["GET"])
@cache.cached()
def threadview(source, thread_id):
    """
    """
    view_query = re.args.get('view')
    posts = Post.query.filter_by(thread_id=thread_id)
    if len(posts.all()) > 0:
        thread = posts[0].forum_thread
        if thread.source != source:
            return re(url_for('threadview', source=thread.source, thread_id=thread_id))
    else:
        return re(url_for('posts', view='threads'))
    if view_query == 'satoshi':
        posts = posts.filter(Post.satoshi_id.isnot(None))
    posts = posts.all()
    prev = ForumThread.query.filter_by(id=thread_id-1).first()
    next = ForumThread.query.filter_by(id=thread_id+1).first()
    app.logger.info(str(re.remote_addr) + ', threads ,' + source + ', ' + str(thread_id))
    return re("threadview.html", posts=posts, prev=prev, next=next)


@app.route('/code/', subdomain="satoshi")
@cache.cached()
def code():
    """
    """
    app.logger.info(str(re.remote_addr) + ', Code')
    return re("code.html")


@app.route('/quotes/', subdomain="satoshi")
@cache.cached()
def quotes():
    """
    """
    app.logger.info(str(re.remote_addr) + ', Quotes')
    categories = QuoteCategory.query.order_by(QuoteCategory.slug).all()
    return re("quotes.html", categories=categories)


# noinspection PyShadowingNames
@app.route('/quotes/<string:slug>/', subdomain="satoshi")
@cache.cached()
def quotescategory(slug):
    """
    """
    app.logger.info(str(re.remote_addr) + ', Quotes')
    order = re.args.get('order')
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
        return re("quotescategory.html", quotes=quotes,
                               category=category, order=order)
    else:
        return re('quotes')


# noinspection PyShadowingNames
@app.route('/authors/', methods=["GET"])
@cache.cached()
def authors():
    """
    """
    authors = Author.query.order_by(Author.last).all()
    app.logger.info(str(re.remote_addr) + ', authors')
    return re("authors.html", authors=authors)


# noinspection PyShadowingNames
@app.route('/authors/<string:authslug>/', methods=["GET"])
@cache.cached()
def author(authslug):
    """
    """
    if authslug.lower() == 'satoshi-nakamoto':
        return re(url_for('satoshi_index'))
    author = Author.query.filter_by(slug=authslug).first()
    if author is not None:
        mem = author.blogposts.all()
        lit = author.docs.all()
        res = author.researchdocs.all()
        app.logger.info(str(re.remote_addr) + ', authors, ' + authslug)
        return re("author.html", author=author, mem=mem, lit=lit,
                               res=res)
    elif not authslug.islower():
        return re(url_for('author', authslug=authslug.lower()))
    else:
        return re(url_for('authors'))


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
    app.logger.info(str(re.remote_addr) + ', literature')
    return re("literature.html", docs=docs, formats=formats)


@app.route('/literature/<string:slug>/', methods=["GET"])
@cache.cached()
def docinfo(slug):
    """
    """
    doc = Doc.query.filter_by(slug=slug).first()
    if doc is not None:
        forms = [form.name for form in doc.formats]
        app.logger.info(str(re.remote_addr) + ', literature, ' + slug)
        return re("docinfo.html", doc=doc, forms=forms,
                               is_lit=True)
    elif ResearchDoc.query.filter_by(slug=slug).first() is not None:
        return re(url_for('researchdocinfo', slug=slug))
    else:
        return re('literature')


@cache.cached()
@app.route('/literature/<int:docid>/', methods=["GET"])
def docinfoid(docid):
    """
    """
    doc = Doc.query.filter_by(id=docid).first()
    if doc is not None:
        return re(url_for('docinfo', slug=doc.slug))
    else:
        doc = ResearchDoc.query.filter_by(lit_id=docid).first()
        if doc is not None:
            return re(url_for('researchdocinfo', slug=doc.slug))
    return re('literature')


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
                return re(url_for('slugview', slug=slug))
            else:
                return re(url_for('static',
                                filename='docs/%(x)s.%(y)s' % {
                                    "x": slug, "y": format
                                }))
        else:
            return re(url_for('docinfo', slug=slug))
    else:
        doc = ResearchDoc.query.filter_by(slug=slug).first()
        if doc is not None:
            return re(url_for('researchdocview', slug=slug))

    return re('literature')


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
                return re(url_for('slugview', slug=slug))
            else:
                return re(url_for('static',
                                filename='docs/%(x)s.%(y)s' % {
                                    "x": slug, "y": format
                                }))
        else:
            return re(url_for('docinfo', slug=doc.slug))
    else:
        doc = ResearchDoc.query.filter_by(lit_id=docid).first()
        if doc is not None:
            return re(url_for('researchdocviewid', id=doc.id))

    return re('literature')


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
    app.logger.info(str(re.remote_addr) + ', research')
    return re('research.html', docs=docs, formats=formats)


@app.route('/research/<string:slug>/', methods=["GET"])
@cache.cached()
def researchdocinfo(slug):
    """
    """
    res = ResearchDoc.query.filter_by(slug=slug).first()
    if res is not None:
        forms = [form.name for form in res.formats]
        app.logger.info(str(re.remote_addr) + ', research, ' + slug)
        return re("docinfo.html", doc=res, forms=forms,
                               is_lit=False)
    else:
        return re('research')


@app.route('/research/<int:resid>/', methods=["GET"])
@cache.cached()
def researchdocinfoid(resid):
    """
    """
    res = ResearchDoc.query.filter_by(id=resid).first()
    if res is not None:
        return re(url_for('researchdocinfo', slug=res.slug))
    else:
        return re('research')


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
                return re(url_for('slugview', slug=slug))
            else:
                return re(url_for('static',
                                filename='docs/%(x)s.%(y)s' % {
                                    "x": slug, "y": format
                                }))
        else:
            return re(url_for('researchdocinfo', slug=slug))
    else:
        return re('literature')


@app.route('/research/<int:resid>/<string:format>/', methods=["GET"])
@cache.cached()
def researchdocviewid(format):
    """
    """
    doc = ResearchDoc.query.filter_by(id=resid).first()
    if doc is not None:
        formats = [form.name for form in doc.formats]
        slug = doc.slug
        if format in formats:
            if format == 'html':
                return re(url_for('slugview', slug=slug))
            else:
                return re(url_for('static',
                                filename='docs/%(x)s.%(y)s' % {
                                    "x": slug, "y": format
                                }))
        else:
            return re(url_for('researchdocinfo', slug=doc.slug))
    else:
        return re('literature')


@app.route('/<string:slug>/', methods=["GET"])
@cache.cached()
def slugview(slug):
    """
    """
    doc = Doc.query.filter_by(slug=slug).first()
    if doc is not None:
        doc.id
        formats = [form.name for form in doc.formats]
        if 'html' in formats:
            app.logger.info(str(re.remote_addr) + ', slugview, ' + slug)
            return re("%s.html" % slug, doc=doc, is_lit=True)
        else:
            return re('literature')
    else:
        doc = ResearchDoc.query.filter_by(slug=slug).first()
        if doc is not None:
            doc.id
            formats = [form.name for form in doc.formats]
            if 'html' in formats:
                app.logger.info(str(re.remote_addr) + ', slugview, ' + slug)
                return re("%s.html" % slug, doc=doc)
            else:
                return re('research')
    return re('literature')


@app.route('/mempool/', methods=["GET"])
@cache.cached()
def blog():
    """
    """
    bps = BlogPost.query.order_by(desc(BlogPost.added)).all()
    app.logger.info(str(re.remote_addr) + ', mempool')
    return re('blog.html', bps=bps)


@app.route('/mempool/<string:slug>/', methods=["GET"])
@cache.cached()
def blogpost(slug):
    """
    """
    # Redirect for new appcoin slug
    if slug == "appcoins-are-fraudulent":
        return re(url_for("blogpost", slug="appcoins-are-snake-oil"))
    bp = BlogPost.query.filter_by(slug=slug).order_by(desc(BlogPost.date)).first()
    lang = Language.query.filter_by(ietf="en").first()
    if bp:
        app.logger.info(str(re.remote_addr) + ', mempool, ' + slug)
        page = pages.get(slug)
        translations = [translation.language for translation in bp.translations]
        translations.sort(key=lambda x: x.name)
        prev = next = None
        if bp.series:
            prev = BlogPost.query.filter_by(
                series=bp.series, series_index=bp.series_index-1).first()
            next = BlogPost.query.filter_by(
                series=bp.series, series_index=bp.series_index+1).first()
        return re('blogpost.html', bp=bp, page=page, lang=lang,
                               translations=translations, prev=prev, next=next)
    else:
        return re(url_for("blog"))


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
            return re(url_for("blogpost", slug=slug))
        elif lang != lang_lower:
            return re(url_for("blogposttrans", slug=slug, lang=lang_lower))
        post_lang = Language.query.filter_by(ietf=lang_lower).first()
        if post_lang not in [translation.language for translation in bp.translations]:
            return re(url_for("blogpost", slug=slug))
        else:
            app.logger.info(str(re.remote_addr) + ', mempool, ' + slug + '-' + lang_lower)
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
            return re('blogpost.html', bp=bp, page=page, lang=post_lang, rtl=rtl,
                                   translations=translations, translators=translators)
    else:
        return re(url_for("blog"))


@app.route('/mempool/series/')
@cache.cached()
def blogseriesindex():
    """
    """
    series = BlogSeries.query.order_by(desc(BlogSeries.id)).all()
    app.logger.info(str(re.remote_addr) + ', Mempool Series')
    return re('blogseriesindex.html', series=series)


@app.route('/mempool/series/<string:slug>/')
@cache.cached()
def blogseries(slug):
    """
    """
    series = BlogSeries.query.filter_by(slug=slug).first()
    if series:
        app.logger.info(str(re.remote_addr) + ', Mempool Series' + ', ' + slug)
        return re('blogseries.html', series=series)
    else:
        return re(url_for('blogseriesindex'))


@app.route('/mempool/feed/')
@cache.cached()
def atomfeed():
    """
    """
    feed = AtomFeed('Mempool | Satoshi Nakamoto Institute',
                    feed_url=re.url, url=re.url_root)
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
    app.logger.info(str(re.remote_addr) + ', atomfeed')
    return feed.get_response()


@app.route('/podcast/', methods=["GET"])
@cache.cached()
def podcast():
    """
    """
    episodes = Episode.query.order_by(desc(Episode.date)).all()
    app.logger.info(str(re.remote_addr) + ', podcast')
    return re('podcast.html', episodes=episodes)


@app.route('/podcast/<string:slug>/', methods=["GET"])
@cache.cached()
def episode(slug):
    """
    """
    ep = Episode.query.filter_by(slug=slug).order_by(desc(Episode.date)).first()
    if ep is not None:
        app.logger.info(str(re.remote_addr) + ', podcast, ' + slug)
        return re('%s.html' % slug, ep=ep)
    else:
        return re(url_for("podcast"))


@app.route('/podcast/feed/', methods=["GET"])
@cache.cached()
def podcastfeed():
    """
    """
    return Response(re('feed.xml'), mimetype='text/xml')


# noinspection PyShadowingNames
@app.route('/the-skeptics/')
#@cache.cached()
def skeptics():
    """
    """
    skeptics = Skeptic.query.order_by(Skeptic.date).all()
    latest_price = Price.query.all()[-1]
    app.logger.info(str(re.remote_addr) + ', the-skeptics')
    return re('the-skeptics.html', skeptics=skeptics, updated=latest_price)


@app.route('/crash-course/', methods=["GET"])
@cache.cached()
def crash_course():
    """
    """
    app.logger.info(str(re.remote_addr) + ', Crash Course')
    return re("crash-course.html")


@app.route('/finney/', methods=["GET"])
@cache.cached()
def finney_index():
    """
    """
    app.logger.info(str(re.remote_addr) + ', Finney')
    docs = Author.query.filter_by(slug='hal-finney').first().docs.all()
    return re("finney_index.html", docs=docs)


@app.route('/finney/rpow/', methods=["GET"])
@cache.cached()
def rpow():
    """
    """
    app.logger.info(str(re.remote_addr) + ', RPOW')
    return re("rpow_index.html")


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
        return re(url_for("docview", slug=doc.slug, format=format))
    else:
        doc = ResearchDoc.query.filter_by(slug=url_slug).first()
        if doc is not None:
            return re(url_for("researchdocview", slug=doc.slug,
                            format=format))
    return re(url_for("index"))


@app.route('/keybase.txt')
@cache.cached()
def static_from_root():
    """
    """
    return send_from_directory(app.static_folder, re.path[1:])
