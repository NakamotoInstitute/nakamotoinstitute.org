from typing import List

from flask import abort, g, jsonify
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
from app.shared.schemas import SlugParamResponse
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

    if not mempool_posts and not library_docs:
        abort(404)

    response_data = AuthorResponse(
        author=author, library=library_docs, mempool=mempool_posts
    )

    return jsonify(response_data.dict(by_alias=True))


@authors.route("/params", methods=["GET"])
@response_model(List[SlugParamResponse])
def get_author_params():
    valid_combinations = []

    authors = db.session.scalars(db.select(Author)).all()
    languages = set(
        db.session.scalars(
            db.select(BlogPostTranslation.language).union(
                db.select(DocumentTranslation.language)
            )
        ).all()
    )

    for author in authors:
        for lang in languages:
            mempool_posts_exist = db.session.scalar(
                db.select(
                    db.exists(
                        db.select(1)
                        .select_from(BlogPostTranslation)
                        .join(BlogPost)
                        .join(blog_post_authors)
                        .where(BlogPostTranslation.language == lang)
                        .where(blog_post_authors.c.author_id == author.id)
                    )
                )
            )

            library_docs_exist = db.session.scalar(
                db.select(
                    db.exists(
                        db.select(1)
                        .select_from(DocumentTranslation)
                        .join(Document)
                        .join(document_authors)
                        .where(DocumentTranslation.language == lang)
                        .where(document_authors.c.author_id == author.id)
                    )
                )
            )

            if mempool_posts_exist or library_docs_exist:
                valid_combinations.append({"slug": author.slug, "locale": lang})

    return valid_combinations
