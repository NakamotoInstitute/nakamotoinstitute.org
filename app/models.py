#
# Satoshi Nakamoto Institute (https://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

from decimal import Decimal

from app import db


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    ietf = db.Column(db.String())
    blog_posts = db.relationship("BlogPostTranslation", back_populates="language")

    def __repr__(self):
        return f"<Language {self.ietf}>"


class EmailThread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    source = db.Column(db.String())
    emails = db.relationship("Email", backref="email_thread", lazy=True)

    def source_to_string(self):
        if self.source == "cryptography":
            return "Cryptography Mailing List"
        else:
            return self.source

    def __repr__(self):
        return f"<EmailThread {self.title}>"


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    satoshi_id = db.Column(db.Integer, unique=True)
    url = db.Column(db.String())
    subject = db.Column(db.String())
    sent_from = db.Column(db.String())
    date = db.Column(db.DateTime)
    text = db.Column(db.String())
    source = db.Column(db.String())
    source_id = db.Column(db.String())
    quotes = db.relationship("Quote", backref="email")
    parent_id = db.Column(db.Integer, db.ForeignKey("email.id"))
    replies = db.relationship(
        "Email", backref=db.backref("parent", remote_side=[id]), lazy="dynamic"
    )
    thread_id = db.Column(db.Integer, db.ForeignKey("email_thread.id"))

    def __repr__(self):
        return f"<Email {self.subject} - {self.source_id}>"


class ForumThread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    url = db.Column(db.String())
    source = db.Column(db.String())
    posts = db.relationship("Post", backref="forum_thread", lazy=True)

    def source_to_string(self):
        if self.source == "bitcointalk":
            return "BitcoinTalk"
        elif self.source == "p2pfoundation":
            return "P2P Foundation"
        else:
            return self.source

    def __repr__(self):
        return f"<ForumThread {self.title}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    satoshi_id = db.Column(db.Integer, unique=True)
    url = db.Column(db.String())
    subject = db.Column(db.String())
    poster_name = db.Column(db.String())
    poster_url = db.Column(db.String())
    post_num = db.Column(db.Integer)  # Post number in thread
    is_displayed = db.Column(db.Boolean)
    nested_level = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    text = db.Column(db.String())
    quotes = db.relationship("Quote", backref="post")
    thread_id = db.Column(db.Integer, db.ForeignKey("forum_thread.id"))

    def __repr__(self):
        return f"<Post {self.subject}>"


quote_categories = db.Table(
    "quote_categories",
    db.Column("quote_id", db.Integer, db.ForeignKey("quote.id")),
    db.Column("quote_category_id", db.Integer, db.ForeignKey("quote_category.id")),
)


class QuoteCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    slug = db.Column(db.String())

    def __repr__(self):
        return f"<QuoteCategory {self.slug}>"


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())
    date = db.Column(db.Date)
    medium = db.Column(db.String())
    email_id = db.Column(db.Integer, db.ForeignKey("email.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.satoshi_id"))
    categories = db.relationship(
        "QuoteCategory",
        secondary=quote_categories,
        backref=db.backref("quotes", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<Quote {self.id}>"


authors = db.Table(
    "authors",
    db.Column("doc_id", db.Integer, db.ForeignKey("doc.id")),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id")),
)

blogauthors = db.Table(
    "blogauthors",
    db.Column("blog_post_id", db.Integer, db.ForeignKey("blog_post.id")),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id")),
)

researchauthors = db.Table(
    "researchauthors",
    db.Column("research_doc_id", db.Integer, db.ForeignKey("research_doc.id")),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id")),
)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String())
    middle = db.Column(db.String())
    last = db.Column(db.String())
    slug = db.Column(db.String())

    def __repr__(self):
        return f"<Author {self.slug}>"

    def __str__(self):
        return f"{self.first} {self.middle} {self.last}"


formats = db.Table(
    "formats",
    db.Column("doc_id", db.Integer, db.ForeignKey("doc.id")),
    db.Column("format_id", db.Integer, db.ForeignKey("format.id")),
)

researchformats = db.Table(
    "researchformats",
    db.Column("research_doc_id", db.Integer, db.ForeignKey("research_doc.id")),
    db.Column("format_id", db.Integer, db.ForeignKey("format.id")),
)


class Format(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return f"<Format {self.name}>"


categories = db.Table(
    "categories",
    db.Column("doc_id", db.Integer, db.ForeignKey("doc.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
)

researchcategories = db.Table(
    "researchcategories",
    db.Column("research_doc_id", db.Integer, db.ForeignKey("research_doc.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return f"<Category {self.name}>"


def get_authors_string(obj):
    if len(obj.author) == 1:
        return str(obj.author[0])
    elif len(obj.author) == 2:
        return f"{obj.author[0]} and {obj.author[1]}"
    else:
        author_string = ""
        for author in obj.author[:-1]:
            author_string += f"{author}, "
        author_string += f"and {author[-1]}"
        return author_string


class Doc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.relationship(
        "Author", secondary=authors, backref=db.backref("docs", lazy="dynamic")
    )
    date = db.Column(db.String())
    slug = db.Column(db.String())
    formats = db.relationship(
        "Format", secondary=formats, backref=db.backref("docs", lazy="dynamic")
    )
    categories = db.relationship(
        "Category", secondary=categories, backref=db.backref("docs", lazy="dynamic")
    )
    doctype = db.Column(db.String())
    external = db.Column(db.String())

    def __repr__(self):
        return f"<Doc {self.title}>"

    @property
    def authors_string(self):
        return get_authors_string(self)


class ResearchDoc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.relationship(
        "Author",
        secondary=researchauthors,
        backref=db.backref("researchdocs", lazy="dynamic"),
    )
    date = db.Column(db.String())
    slug = db.Column(db.String())
    formats = db.relationship(
        "Format",
        secondary=researchformats,
        backref=db.backref("researchdocs", lazy="dynamic"),
    )
    categories = db.relationship(
        "Category",
        secondary=researchcategories,
        backref=db.backref("researchdocs", lazy="dynamic"),
    )
    doctype = db.Column(db.String())
    external = db.Column(db.String())
    lit_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<ResearchDoc {self.title}>"

    @property
    def authors_string(self):
        return get_authors_string(self)


blog_post_translators = db.Table(
    "blog_post_translators",
    db.Column("translator_id", db.Integer, db.ForeignKey("translator.id")),
    db.Column(
        "blog_post_translation_id",
        db.Integer,
        db.ForeignKey("blog_post_translation.id"),
    ),
)


class Translator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    url = db.Column(db.String())
    blog_posts = db.relationship(
        "BlogPostTranslation",
        secondary=blog_post_translators,
        back_populates="translators",
    )

    def __repr__(self):
        return f"<Translator {self.name}>"


class BlogPostTranslation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_post_id = db.Column(db.Integer, db.ForeignKey("blog_post.id"))
    language_id = db.Column(db.Integer, db.ForeignKey("language.id"))
    blog_post = db.relationship("BlogPost", back_populates="translations")
    language = db.relationship("Language", back_populates="blog_posts")
    translators = db.relationship(
        "Translator", secondary=blog_post_translators, back_populates="blog_posts"
    )

    def __repr__(self):
        return f"<BlogPostTranslation {self.blog_post.slug} - {self.language.ietf}>"


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.relationship(
        "Author", secondary=blogauthors, backref=db.backref("blogposts", lazy="dynamic")
    )
    date = db.Column(db.Date)
    added = db.Column(db.Date)
    slug = db.Column(db.String())
    excerpt = db.Column(db.String())
    translations = db.relationship("BlogPostTranslation", back_populates="blog_post")
    series_id = db.Column(db.Integer, db.ForeignKey("blog_series.id"))
    series_index = db.Column(db.Integer)

    def __repr__(self):
        return f"<BlogPost {self.title}>"


class BlogSeries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    slug = db.Column(db.String())
    chapter_title = db.Column(db.Boolean)
    blogposts = db.relationship("BlogPost", backref=db.backref("series"))

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<BlogSeries {self.title}>"


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
    media_embed = db.Column(db.String())
    twitter_screenshot = db.Column(db.Boolean)
    waybacklink = db.Column(db.String())
    slug = db.Column(db.String())
    _btc_balance = db.Column(db.String())
    _usd_invested = db.Column(db.Integer)
    _usd_value = db.Column(db.String())
    _percent_change = db.Column(db.String())

    @property
    def btc_balance(self):
        return Decimal(self._btc_balance)

    @property
    def usd_invested(self):
        return Decimal(self._usd_invested)

    @property
    def usd_value(self):
        return Decimal(self._usd_value)

    @property
    def percent_change(self):
        return Decimal(self._percent_change)

    def __repr__(self):
        return f"<Skeptic {self.name}>"


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    date = db.Column(db.Date())
    duration = db.Column(db.String())
    subtitle = db.Column(db.String())
    summary = db.Column(db.String())
    slug = db.Column(db.String())
    youtube = db.Column(db.String())
    length = db.Column(db.String())
    time = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return f"<Episode {self.title}>"


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    price = db.Column(db.String())

    def __repr__(self):
        return f"<Price {self.date}>"

    def serialize(self):
        return {
            "id": self.id,
            "date": str(self.date),
            "price": self.price,
        }
