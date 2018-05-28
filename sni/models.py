#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

from sni import db, app


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String())
    sent_from = db.Column(db.String())
    date = db.Column(db.DateTime)
    text = db.Column(db.String())
    source = db.Column(db.String())
    quotes = db.relationship("Quote", backref="email")

    def __repr__(self):
        return '<Email %r>' % (self.subject)


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    url = db.Column(db.String())
    source = db.Column(db.String())
    posts = db.relationship('Post', backref='thread', lazy=True)

    def __repr__(self):
        return '<Thread %r>' % (self.title)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    satoshi_id = db.Column(db.Integer)
    url = db.Column(db.String())
    subject = db.Column(db.String())
    poster_name = db.Column(db.String())
    poster_url = db.Column(db.String())
    post_num = db.Column(db.Integer) # Post number in thread
    is_displayed = db.Column(db.Boolean)
    nested_level = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    text = db.Column(db.String())
    quotes = db.relationship("Quote", backref="post")
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))

    def __repr__(self):
        return '<Post %r>' % (self.subject)

quote_categories = db.Table(
    'quote_categories',
    db.Column('quote_id', db.Integer, db.ForeignKey('quote.id')),
    db.Column('quote_category_id', db.Integer, db.ForeignKey('quote_category.id'))
)


class QuoteCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    slug = db.Column(db.String())

    def __repr__(self):
        return '<QuoteCategory %r>' % (self.slug)


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())
    date = db.Column(db.Date)
    medium = db.Column(db.String())
    email_id = db.Column(db.Integer, db.ForeignKey('email.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.satoshi_id'))
    categories = db.relationship('QuoteCategory',
                                 secondary=quote_categories,
                                 backref=db.backref('quotes', lazy='dynamic'))

    def __repr__(self):
        return '<Quote %r>' % (self.id)


authors = db.Table(
    'authors',
    db.Column('doc_id', db.Integer, db.ForeignKey('doc.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)

blogauthors = db.Table(
    'blogauthors',
    db.Column('blog_post_id', db.Integer, db.ForeignKey('blog_post.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)

researchauthors = db.Table(
    'researchauthors',
    db.Column('research_doc_id', db.Integer, db.ForeignKey('research_doc.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String())
    middle = db.Column(db.String())
    last = db.Column(db.String())
    slug = db.Column(db.String())

    def __repr__(self):
        return '<Author %r>' % (self.slug)

formats = db.Table(
    'formats',
    db.Column('doc_id', db.Integer, db.ForeignKey('doc.id')),
    db.Column('format_id', db.Integer, db.ForeignKey('format.id'))
)

researchformats = db.Table(
    'researchformats',
    db.Column('research_doc_id', db.Integer, db.ForeignKey('research_doc.id')),
    db.Column('format_id', db.Integer, db.ForeignKey('format.id'))
)


class Format(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return '<Format %r>' % (self.name)

categories = db.Table(
    'categories',
    db.Column('doc_id', db.Integer, db.ForeignKey('doc.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')))

researchcategories = db.Table(
    'researchcategories',
    db.Column('research_doc_id', db.Integer, db.ForeignKey('research_doc.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return '<Category %r>' % (self.name)


class Doc(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    author = db.relationship('Author',
                             secondary=authors,
                             backref=db.backref('docs', lazy='dynamic'))
    date = db.Column(db.String())
    slug = db.Column(db.String())
    formats = db.relationship('Format',
                              secondary=formats,
                              backref=db.backref('docs', lazy='dynamic'))
    categories = db.relationship('Category',
                                 secondary=categories,
                                 backref=db.backref('docs', lazy='dynamic'))
    doctype = db.Column(db.String())
    external = db.Column(db.String())

    def __repr__(self):
        return '<Doc %r>' % (self.title)


class ResearchDoc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.relationship('Author',
                             secondary=researchauthors,
                             backref=db.backref('researchdocs', lazy='dynamic'))
    date = db.Column(db.String())
    slug = db.Column(db.String())
    formats = db.relationship('Format',
                              secondary=researchformats,
                              backref=db.backref('researchdocs', lazy='dynamic'))
    categories = db.relationship('Category',
                                 secondary=researchcategories,
                                 backref=db.backref('researchdocs', lazy='dynamic'))
    doctype = db.Column(db.String())
    external = db.Column(db.String())
    lit_id = db.Column(db.Integer)

    def __repr__(self):
        return '<ResearchDoc %r>' % (self.title)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.relationship('Author',
                             secondary=blogauthors,
                             backref=db.backref('blogposts', lazy='dynamic'))
    date = db.Column(db.Date)
    added = db.Column(db.Date)
    slug = db.Column(db.String())
    excerpt = db.Column(db.String())
    languages = db.Column(db.String())

    def __repr__(self):
        return '<BlogPost %r>' % (self.title)


class Skeptic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    title = db.Column(db.String())
    article = db.Column(db.String())
    date = db.Column(db.Date)
    source = db.Column(db.String())
    excerpt = db.Column(db.String())
    price = db.Column(db.String())
    link = db.Column(db.String())
    waybacklink = db.Column(db.String())
    slug = db.Column(db.String())

    def __repr__(self):
        return '<Skeptic %r>' % (self.name)


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    date = db.Column(db.Date())
    duration = db.Column(db.String())
    subtitle = db.Column(db.String())
    summary = db.Column(db.String())
    slug = db.Column(db.String())
    youtube = db.Column(db.String())
    address = db.Column(db.String())
    length = db.Column(db.String())
    time = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '<Episode %r>' % (self.title)


class DonationAddress(db.Model):
    address = db.Column(db.String, primary_key=True)
    lastseen = db.Column(db.DateTime)
