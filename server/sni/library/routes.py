from typing import List

from flask import Blueprint, g

from sni.extensions import db
from sni.models import DocumentTranslation
from sni.shared.schemas import SlugParamModel
from sni.utils.decorators import response_model

from .schemas import DocumentIndexModel, DocumentModel

blueprint = Blueprint("library", __name__, url_prefix="/library")


@blueprint.route("/", methods=["GET"])
@response_model(List[DocumentIndexModel])
def get_library_docs():
    docs = db.session.scalars(
        db.select(DocumentTranslation)
        .filter(DocumentTranslation.locale == g.locale)
        .order_by(DocumentTranslation.sort_title.asc())
    ).all()
    return docs


@blueprint.route("/<string:slug>", methods=["GET"])
@response_model(DocumentModel)
def get_library_doc(slug):
    post = db.first_or_404(
        db.select(DocumentTranslation).filter_by(slug=slug, locale=g.locale)
    )
    return post


@blueprint.route("/params", methods=["GET"])
@response_model(List[SlugParamModel])
def get_library_params():
    posts = db.session.scalars(db.select(DocumentTranslation)).all()
    return [{"locale": post.locale, "slug": post.slug} for post in posts]
