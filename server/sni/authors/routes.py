from typing import List

from flask import abort, g, jsonify
from sqlalchemy import or_

from sni import db
from sni.models import (
    Author,
    BlogPost,
    BlogPostTranslation,
    Document,
    DocumentTranslation,
    blog_post_authors,
    document_authors,
)
from sni.shared.schemas import SlugParamModel
from sni.utils.decorators import response_model

from . import authors
from .schemas import AuthorDetailModel, AuthorModel


@authors.route("/", methods=["GET"])
@response_model(List[AuthorModel])
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
                DocumentTranslation.locale == g.locale,
                BlogPostTranslation.locale == g.locale,
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
        .filter(Author.id == author.id, BlogPostTranslation.locale == g.locale)
    ).all()

    library_docs = db.session.scalars(
        db.select(DocumentTranslation)
        .join(Document)
        .join(document_authors)
        .join(Author)
        .filter(Author.id == author.id, DocumentTranslation.locale == g.locale)
    ).all()

    if not mempool_posts and not library_docs:
        abort(404)

    response_data = AuthorDetailModel(
        author=author, library=library_docs, mempool=mempool_posts
    )

    return jsonify(response_data.dict(by_alias=True))


@authors.route("/params", methods=["GET"])
@response_model(List[SlugParamModel])
def get_author_params():
    valid_combinations = []

    authors = db.session.scalars(db.select(Author)).all()
    locales = set(
        db.session.scalars(
            db.select(BlogPostTranslation.locale).union(
                db.select(DocumentTranslation.locale)
            )
        ).all()
    )

    for author in authors:
        for locale in locales:
            mempool_posts_exist = db.session.scalar(
                db.select(
                    db.exists(
                        db.select(1)
                        .select_from(BlogPostTranslation)
                        .join(BlogPost)
                        .join(blog_post_authors)
                        .where(BlogPostTranslation.locale == locale)
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
                        .where(DocumentTranslation.locale == locale)
                        .where(document_authors.c.author_id == author.id)
                    )
                )
            )

            if mempool_posts_exist or library_docs_exist:
                valid_combinations.append({"slug": author.slug, "locale": locale})

    return valid_combinations
