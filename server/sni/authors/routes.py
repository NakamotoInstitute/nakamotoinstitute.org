from typing import List

from flask import Blueprint, abort, g, jsonify
from sqlalchemy import or_
from sqlalchemy.orm import aliased

from sni.extensions import db
from sni.library.models import Document, DocumentTranslation, document_authors
from sni.mempool.models import (
    BlogPost,
    BlogPostTranslation,
    blog_post_authors,
)
from sni.shared.schemas import SlugParamModel
from sni.utils.decorators import response_model

from .models import Author
from .schemas.base import AuthorModel
from .schemas.response import AuthorDetailModel

blueprint = Blueprint("authors", __name__, url_prefix="/authors")


@blueprint.route("/", methods=["GET"])
@response_model(List[AuthorModel])
def get_authors():
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)
    authors = db.session.scalars(
        db.select(Author)
        .outerjoin(document_authors)
        .outerjoin(Document)
        .outerjoin(DocumentTranslationAlias)
        .outerjoin(blog_post_authors)
        .outerjoin(BlogPost)
        .outerjoin(BlogPostTranslationAlias)
        .filter(
            or_(
                DocumentTranslationAlias.locale == g.locale,
                BlogPostTranslationAlias.locale == g.locale,
            )
        )
        .order_by(Author.sort_name)
        .distinct()
    ).all()

    return authors


@blueprint.route("/<string:slug>", methods=["GET"])
def get_author(slug):
    author = db.first_or_404(db.select(Author).filter_by(slug=slug))

    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)

    mempool_posts = db.session.scalars(
        db.select(BlogPostTranslationAlias)
        .join(BlogPost)
        .join(blog_post_authors)
        .join(Author)
        .filter(Author.id == author.id, BlogPostTranslationAlias.locale == g.locale)
    ).all()

    library_docs = db.session.scalars(
        db.select(DocumentTranslationAlias)
        .join(Document)
        .join(document_authors)
        .join(Author)
        .filter(Author.id == author.id, DocumentTranslationAlias.locale == g.locale)
    ).all()

    if not mempool_posts and not library_docs:
        abort(404)

    response_data = AuthorDetailModel(
        author=author, library=library_docs, mempool=mempool_posts
    )

    return jsonify(response_data.dict(by_alias=True))


@blueprint.route("/params", methods=["GET"])
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

    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)

    for author in authors:
        for locale in locales:
            mempool_posts_exist = db.session.scalar(
                db.select(
                    db.exists(
                        db.select(1)
                        .select_from(BlogPostTranslationAlias)
                        .join(BlogPost)
                        .join(blog_post_authors)
                        .where(BlogPostTranslationAlias.locale == locale)
                        .where(blog_post_authors.c.author_id == author.id)
                    )
                )
            )

            library_docs_exist = db.session.scalar(
                db.select(
                    db.exists(
                        db.select(1)
                        .select_from(DocumentTranslationAlias)
                        .join(Document)
                        .join(document_authors)
                        .where(DocumentTranslationAlias.locale == locale)
                        .where(document_authors.c.author_id == author.id)
                    )
                )
            )

            if mempool_posts_exist or library_docs_exist:
                valid_combinations.append({"slug": author.slug, "locale": locale})

    return valid_combinations
