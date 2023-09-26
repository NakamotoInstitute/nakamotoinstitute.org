from typing import List

from flask import g, jsonify
from sqlalchemy import or_

from app import db
from app.models import (
    Author,
    BlogPost,
    BlogPostTranslation,
    Document,
    DocumentTranslation,
    blog_post_authors,
    document_authors,
)
from app.utils.decorators import response_model

from . import authors
from .schemas import AuthorResponse, AuthorSchema


@authors.route("/", methods=["GET"])
@response_model(List[AuthorSchema])
def get_authors():
    authors = db.session.scalars(
        db.select(Author)
        .outerjoin(document_authors)
        .outerjoin(Document)
        .outerjoin(DocumentTranslation)
        .outerjoin(blog_post_authors)
        .outerjoin(BlogPost)
        .outerjoin(BlogPostTranslation)
        .filter(
            or_(
                DocumentTranslation.language == g.locale,
                BlogPostTranslation.language == g.locale,
            )
        )
        .order_by(Author.sort_name)
        .distinct()
    ).all()

    return authors


@authors.route("/<string:slug>", methods=["GET"])
def get_author(slug):
    author = db.first_or_404(db.select(Author).filter_by(slug=slug))

    mempool_posts = db.session.scalars(
        db.select(BlogPostTranslation)
        .join(BlogPost)
        .join(blog_post_authors)
        .join(Author)
        .filter(Author.id == author.id, BlogPostTranslation.language == g.locale)
    ).all()

    library_docs = db.session.scalars(
        db.select(DocumentTranslation)
        .join(Document)
        .join(document_authors)
        .join(Author)
        .filter(Author.id == author.id, DocumentTranslation.language == g.locale)
    ).all()

    response_data = AuthorResponse(
        author=author, library=library_docs, mempool=mempool_posts
    )

    return jsonify(response_data.dict())
