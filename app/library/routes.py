from typing import List

from flask import g

from app import db
from app.models import DocumentTranslation
from app.shared.schemas import SlugParamModel
from app.utils.decorators import response_model

from . import library
from .schemas import DocumentIndexModel, DocumentModel


@library.route("/", methods=["GET"])
@response_model(List[DocumentIndexModel])
def get_library_docs():
    docs = db.session.scalars(
        db.select(DocumentTranslation)
        .filter(DocumentTranslation.locale == g.locale)
        .order_by(DocumentTranslation.sort_title.asc())
    ).all()
    return docs


@library.route("/<string:slug>", methods=["GET"])
@response_model(DocumentModel)
def get_library_doc(slug):
    post = db.first_or_404(
        db.select(DocumentTranslation).filter_by(slug=slug, locale=g.locale)
    )
    return post


@library.route("/params", methods=["GET"])
@response_model(List[SlugParamModel])
def get_library_params():
    posts = db.session.scalars(db.select(DocumentTranslation)).all()
    return [{"locale": post.locale, "slug": post.slug} for post in posts]
