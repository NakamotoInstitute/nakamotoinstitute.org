
#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

from sni import app, db, cache
from models import Post, Email, Doc, ResearchDoc, Author, Format, Category,\
                   BlogPost, Skeptic, DonationAddress, Episode, Quote, QuoteCategory
from flask import render_template, json, url_for, redirect, request, Response,\
                  send_from_directory
from sqlalchemy import asc, desc
from werkzeug.contrib.atom import AtomFeed
from datetime import datetime
import os
import re

from jinja2 import evalcontextfilter, Markup, escape

@app.errorhandler(404)
def internal_error(error):
    app.logger.error(str(request.remote_addr) + ', 404')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(str(request.remote_addr) + ', 500')
    return render_template('500.html'), 500

@app.route("/", subdomain="satoshi")
def satoshi_index():
    app.logger.info(str(request.remote_addr) + ', SatoshiIndex')
    return render_template("satoshiindex.html")

@app.route('/')
def index():
    bp = BlogPost.query.order_by(desc(BlogPost.added)).first()
    app.logger.info(str(request.remote_addr) + ', Index')
    return render_template("index.html", bp=bp)

@app.route('/about/', methods = ["GET"])
def about():
    app.logger.info(str(request.remote_addr) + ', About')
    return render_template("about.html")

@app.route('/contact/', methods = ["GET"])
def contact():
    app.logger.info(str(request.remote_addr) + ', Contact')
    return render_template("contact.html")

@cache.cached(timeout=900)
@app.route('/emails/', subdomain="satoshi", methods = ["GET"])
@app.route('/emails/cryptography/', subdomain="satoshi", methods = ["GET"])
def emails():
    emails = Email.query.order_by(Email.date).all()
    app.logger.info(str(request.remote_addr) + ', Emails')
    return render_template("emails.html", emails=emails)

@cache.cached(timeout=900)
@app.route('/emails/cryptography/<int:emnum>/', subdomain="satoshi", methods = ["GET"])
def emailview(emnum):
    email = Email.query.filter_by(id=emnum).first()
    prev = Email.query.filter_by(id=emnum-1).first()
    next = Email.query.filter_by(id=emnum+1).first()
    if(email!=None):
        app.logger.info(str(request.remote_addr) + ', Emails, ' + str(emnum))
        return render_template("emailview.html", email=email, prev=prev, next=next)
    else:
        return redirect('emails')

@cache.cached(timeout=900)
@app.route('/posts/', subdomain="satoshi", methods = ["GET"])
def posts():
    posts = Post.query.order_by(Post.date).all()
    app.logger.info(str(request.remote_addr) + ', posts')
    return render_template("posts.html", posts=posts, source=None)

@cache.cached(timeout=900)
@app.route('/posts/<string:source>/', subdomain="satoshi", methods = ["GET"])
def forumposts(source):
    posts = Post.query.filter_by(source=source).order_by(Post.date).all()
    if(len(posts)!=0):
        app.logger.info(str(request.remote_addr) + ', posts, ' + source)
        return render_template("posts.html", posts=posts, source=source)
    else:
        return redirect(url_for('posts'))

@cache.cached(timeout=900)
@app.route('/posts/<string:source>/<int:postnum>/', subdomain="satoshi", methods=["GET"])
def postview(postnum,source):
    post = Post.query.filter_by(id=postnum, source=source).first()
    prev = Post.query.filter_by(id=postnum-1, source=source).first()
    next = Post.query.filter_by(id=postnum+1, source=source).first()
    if(post!=None):
        app.logger.info(str(request.remote_addr) + ', posts ,' + source + ', ' + str(postnum))
        return render_template("postview.html", post=post, prev=prev, next=next)
    else:
        return redirect('posts')

@cache.cached(timeout=900)
@app.route('/code/', subdomain="satoshi")
def code():
    app.logger.info(str(request.remote_addr) + ', Code')
    return render_template("code.html")

@cache.cached(timeout=900)
@app.route('/quotes/', subdomain="satoshi")
def quotes():
    app.logger.info(str(request.remote_addr) + ', Quotes')
    categories = QuoteCategory.query.order_by(QuoteCategory.slug).all()
    return render_template("quotes.html", categories=categories)

@cache.cached(timeout=900)
@app.route('/quotes/<string:slug>/', subdomain="satoshi")
def quotescategory(slug):
    app.logger.info(str(request.remote_addr) + ', Quotes')
    order = request.args.get('order')
    if order == 'desc':
        quotes = Quote.query.filter(Quote.categories.any(slug=slug)).order_by(desc(Quote.date)).all()
    else:
        quotes = Quote.query.filter(Quote.categories.any(slug=slug)).order_by(Quote.date).all()
    category = QuoteCategory.query.filter_by(slug=slug).first()
    return render_template("quotescategory.html", quotes=quotes, category=category, order=order)

@cache.cached(timeout=900)
@app.route('/authors/', methods=["GET"])
def authors():
    authors = Author.query.order_by(Author.last).all()
    app.logger.info(str(request.remote_addr) + ', authors')
    return render_template("authors.html", authors=authors)

@cache.cached(timeout=900)
@app.route('/authors/<string:authslug>/', methods=["GET"])
def author(authslug):
    if (authslug.lower()=='satoshi-nakamoto'):
        return redirect(url_for('satoshi_index'))
    author = Author.query.filter_by(slug=authslug).first()
    if (author!=None):
        mem = author.blogposts.all()
        lit = author.docs.all()
        res = author.researchdocs.all()
        app.logger.info(str(request.remote_addr) + ', authors, ' + authslug)
        return render_template("author.html", author=author, mem=mem, lit=lit, res=res)
    elif (not authslug.islower()):
        return redirect(url_for('author', authslug=authslug.lower()))
    else:
        return redirect(url_for('index'))

@cache.cached(timeout=900)
@app.route('/literature/', methods=["GET"])
def literature():
    docs = Doc.query.order_by('id').all()
    formats = {}
    for doc in docs:
        formlist = []
        for format in doc.formats:
            formlist += [format.name]
        formats[doc.slug] = formlist
    app.logger.info(str(request.remote_addr) + ', literature')
    return render_template("literature.html", docs=docs, formats=formats)

@cache.cached(timeout=900)
@app.route('/literature/<string:slug>/', methods=["GET"])
def docinfo(slug):
    doc = Doc.query.filter_by(slug=slug).first()
    if(doc!=None):
        forms = []
        for form in doc.formats:
            if form.name == 'html':
                forms += ['html']
            if form.name == 'pdf':
                forms += ['pdf']
            if form.name == 'txt':
                forms += ['txt']
            if form.name == 'unavailable':
                forms += ['una']
            if form.name == 'ext':
                forms += ['ext']
        app.logger.info(str(request.remote_addr) + ', literature, ' + slug)
        return render_template("docinfo.html",doc=doc, forms=forms, is_lit=True)
    elif (ResearchDoc.query.filter_by(slug=slug).first() != None):
        return redirect(url_for('researchdocinfo', slug=slug))
    else:
        return redirect('literature')

@cache.cached(timeout=900)
@app.route('/literature/<int:docid>/', methods=["GET"])
def docinfoid(docid):
    doc = Doc.query.filter_by(id=docid).first()
    if(doc!=None):
        forms = []
        for form in doc.formats:
            if form.name == 'html':
                forms += ['html']
            if form.name == 'pdf':
                forms += ['pdf']
            if form.name == 'txt':
                forms += ['txt']
            if form.name == 'unavailable':
                forms += ['una']
        return redirect(url_for('docinfo', slug=doc.slug))
    else:
        doc = ResearchDoc.query.filter_by(lit_id=docid).first()
        if (doc != None):
            return redirect(url_for('researchdocinfo', slug=doc.slug))

    return redirect('literature')

@cache.cached(timeout=900)
@app.route('/literature/<string:slug>/<string:format>/', methods=["GET"])
def s(slug, format):
    doc = Doc.query.filter_by(slug=slug).first()
    if(doc!=None):
        formats = []
        for form in doc.formats:
            formats += [form.name]
        if format in formats:
            if(format=='html'):
                return redirect(url_for('slugview', slug=slug))
            else:
                return redirect(url_for('static', filename='docs/%(x)s.%(y)s' % {"x": slug, "y": format}))
        else:
            return redirect(url_for('docinfo', slug=slug))
    else:
        doc = ResearchDoc.query.filter_by(slug=slug).first()
        if (doc != None):
            return redirect(url_for('researchdocview', slug=slug))

    return redirect('literature')

@cache.cached(timeout=900)
@app.route('/literature/<int:docid>/<string:format>/', methods=["GET"])
def docviewid(docid, format):
    doc = Doc.query.filter_by(id=docid).first()
    if(doc!=None):
        formats = []
        for form in doc.formats:
            formats += [form.name]
        slug = doc.slug
        if format in formats:
            if(format=='html'):
                return redirect(url_for('slugview', slug=slug))
            else:
                return redirect(url_for('static', filename='docs/%(x)s.%(y)s' % {"x": slug, "y": format}))
        else:
            return redirect(url_for('docinfo', slug=doc.slug))
    else:
        doc = ResearchDoc.query.filter_by(lit_id=docid).first()
        if (doc != None):
            return redirect(url_for('researchdocviewid', id=doc.id))

    return redirect('literature')

@cache.cached(timeout=900)
@app.route('/research/', methods=["GET"])
def research():
    docs = ResearchDoc.query.order_by('id').all()
    formats = {}
    for doc in docs:
        formlist = []
        for format in doc.formats:
            formlist += [format.name]
        formats[doc.slug] = formlist
    app.logger.info(str(request.remote_addr) + ', research')
    return render_template('research.html', docs=docs, formats=formats)

@cache.cached(timeout=900)
@app.route('/research/<string:slug>/', methods=["GET"])
def researchdocinfo(slug):
    res = ResearchDoc.query.filter_by(slug=slug).first()
    if(res!=None):
        forms = []
        for form in res.formats:
            if form.name == 'html':
                forms += ['html']
            if form.name == 'pdf':
                forms += ['pdf']
            if form.name == 'txt':
                forms += ['txt']
            if form.name == 'unavailable':
                forms += ['una']
            if form.name == 'ext':
                forms += ['ext']
        app.logger.info(str(request.remote_addr) + ', research, ' + slug)
        return render_template("docinfo.html", doc=res, forms=forms, is_lit=False)
    else:
        return redirect('research')

@cache.cached(timeout=900)
@app.route('/research/<int:resid>/', methods=["GET"])
def researchdocinfoid(resid):
    res = ResearchDoc.query.filter_by(id=resid).first()
    if(res!=None):
        forms = []
        for form in res.formats:
            if form.name == 'html':
                forms += ['html']
            if form.name == 'pdf':
                forms += ['pdf']
            if form.name == 'txt':
                forms += ['txt']
            if form.name == 'unavailable':
                forms += ['una']
        return redirect(url_for('researchdocinfo', slug=res.slug))
    else:
        return redirect('research')

@cache.cached(timeout=900)
@app.route('/research/<string:slug>/<string:format>/', methods=["GET"])
def researchdocview(slug, format):
    doc = ResearchDoc.query.filter_by(slug=slug).first()
    if(doc!=None):
        formats = []
        for form in doc.formats:
            formats += [form.name]
        if format in formats:
            if(format=='html'):
                return redirect(url_for('slugview', slug=slug))
            else:
                return redirect(url_for('static', filename='docs/%(x)s.%(y)s' % {"x": slug, "y": format}))
        else:
            return redirect(url_for('researchdocinfo', slug=slug))
    else:
        return redirect('literature')

@cache.cached(timeout=900)
@app.route('/research/<int:resid>/<string:format>/', methods=["GET"])
def researchdocviewid(docid, format):
    doc = ResearchDoc.query.filter_by(id=resid).first()
    if(doc!=None):
        formats = []
        for form in doc.formats:
            formats += [form.name]
        slug = doc.slug
        if format in formats:
            if(format=='html'):
                return redirect(url_for('slugview', slug=slug))
            else:
                return redirect(url_for('static', filename='docs/%(x)s.%(y)s' % {"x": slug, "y": format}))
        else:
            return redirect(url_for('researchdocinfo', slug=doc.slug))
    else:
        return redirect('literature')

@cache.cached(timeout=900)
@app.route('/<string:slug>/', methods=["GET"])
def slugview(slug):
    doc = Doc.query.filter_by(slug=slug).first()
    if(doc!=None):
        docid = doc.id
        formats = []
        for form in doc.formats:
            formats += [form.name]
        if('html' in formats):
            app.logger.info(str(request.remote_addr) + ', slugview, ' + slug)
            return render_template("%s.html" % slug, doc=doc, is_lit=True)
        else:
            return redirect('literature')
    else:
        doc = ResearchDoc.query.filter_by(slug=slug).first()
        if(doc!=None):
            docid = doc.id
            formats = []
            for form in doc.formats:
                formats += [form.name]
            if('html' in formats):
                app.logger.info(str(request.remote_addr) + ', slugview, ' + slug)
                return render_template("%s.html" % slug, doc=doc)
            else:
                return redirect('research')
    return redirect('literature')


@cache.cached(timeout=900)
@app.route('/mempool/', methods=["GET"])
def blog():
    bps = BlogPost.query.order_by(desc(BlogPost.added)).all()
    app.logger.info(str(request.remote_addr) + ', mempool')
    return render_template('blog.html', bps=bps)

@cache.cached(timeout=900)
@app.route('/mempool/<string:slug>/', methods=["GET"])
def blogpost(slug):
    # Redirect for new appcoin slug
    if slug == "appcoins-are-fraudulent":
        return redirect(url_for("blogpost", slug="appcoins-are-snake-oil"))
    bp = BlogPost.query.filter_by(slug=slug).order_by(desc(BlogPost.date)).first()
    if(bp != None):
        app.logger.info(str(request.remote_addr) + ', mempool, ' + slug)
        return render_template('%s.html' % slug, bp=bp, lang='en')
    else:
        return redirect(url_for("blog"))

@cache.cached(timeout=900)
@app.route('/mempool/<string:slug>/<string:lang>/', methods=["GET"])
def blogposttrans(slug, lang):
    bp = BlogPost.query.filter_by(slug=slug).order_by(desc(BlogPost.date)).first()
    lang = lang.lower()
    if(bp != None):
        languages = bp.languages.split(', ')
        if(lang == 'en' or all(lang != l for l in languages)):
            return redirect(url_for("blogpost", slug=slug))
        else:
            app.logger.info(str(request.remote_addr) + ', mempool, ' + slug+'-'+lang)
            return render_template('%s-%s.html' % (slug, lang), bp=bp, lang=lang)
    else:
        return redirect(url_for("blog"))

@cache.cached(timeout=900)
@app.route('/mempool/feed/')
def atomfeed():
    feed = AtomFeed('Mempool | Satoshi Nakamoto Institute',
                    feed_url=request.url, url=request.url_root)
    articles = BlogPost.query.order_by(desc(BlogPost.added)).all()
    for article in articles:
        articleurl = url_for('blogpost', slug=article.slug, _external=True)
        content = article.excerpt + "<br><br><a href='"+articleurl+"'>Read more...</a>"
        feed.add(article.title, unicode(content),
                 content_type='html',
                 author=article.author[0].first + ' ' + article.author[0].last,
                 url=articleurl,
                 updated=article.added,
                 published=article.date)
    app.logger.info(str(request.remote_addr) + ', atomfeed')
    return feed.get_response()

@cache.cached(timeout=900)
@app.route('/podcast/', methods=["GET"])
def podcast():
    episodes = Episode.query.order_by(desc(Episode.date)).all()
    app.logger.info(str(request.remote_addr) + ', podcast')
    return render_template('podcast.html', episodes=episodes)

@cache.cached(timeout=900)
@app.route('/podcast/<string:slug>/', methods=["GET"])
def episode(slug):
    ep = Episode.query.filter_by(slug=slug).order_by(desc(Episode.date)).first()
    if(ep != None):
        app.logger.info(str(request.remote_addr) + ', podcast, ' + slug)
        return render_template('%s.html' % slug, ep=ep)
    else:
        return redirect(url_for("podcast"))

@cache.cached(timeout=900)
@app.route('/podcast/feed/', methods=["GET"])
def podcastfeed():
    return Response(render_template('feed.xml'), mimetype='text/xml')


@cache.cached(timeout=900)
@app.route('/the-skeptics/')
def skeptics():
    skeptics = Skeptic.query.order_by(Skeptic.date).all()
    app.logger.info(str(request.remote_addr) + ', the-skeptics')
    return render_template('the-skeptics.html', skeptics=skeptics)

@cache.cached(timeout=900)
@app.route('/crash-course/', methods=["GET"])
def crash_course():
    app.logger.info(str(request.remote_addr) + ', Crash Course')
    return render_template("crash-course.html")

@cache.cached(timeout=900)
@app.route('/finney/', methods=["GET"])
def finney_index():
    app.logger.info(str(request.remote_addr) + ', Finney')
    docs = Author.query.filter_by(slug='hal-finney').first().docs.all()
    return render_template("finney_index.html", docs=docs)

@cache.cached(timeout=900)
@app.route('/finney/rpow/', methods=["GET"])
def rpow():
    app.logger.info(str(request.remote_addr) + ', RPOW')
    return render_template("rpow_index.html")

@app.route('/finney/rpow/<path:path>')
def rpow_site(path):
  return app.send_static_file('rpow/' + path)

# Redirect old links
@cache.cached(timeout=900)
@app.route('/<string:url_slug>.<string:format>/')
def reroute(url_slug, format):
    doc=Doc.query.filter_by(slug=url_slug).first()
    if(doc!=None):
        return redirect(url_for("docview", slug=doc.slug, format=format))
    else:
        doc = ResearchDoc.query.filter_by(slug=url_slug).first()
        if (doc != None):
            return redirect(url_for("researchdocview", slug=doc.slug, format=format))
    return redirect(url_for("index"))
