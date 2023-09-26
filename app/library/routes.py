from typing import List

from flask import g

from app import db
from app.models import DocumentTranslation
from app.utils.decorators import response_model

from . import library
from .schemas import LibraryDocBaseSchema, LibraryDocSchema


@library.route("/", methods=["GET"])
@response_model(List[LibraryDocBaseSchema])
def get_library_docs():
    docs = db.session.scalars(
        db.select(DocumentTranslation)
        .filter(DocumentTranslation.language == g.locale)
        .order_by(DocumentTranslation.sort_title.asc())
    ).all()
    return docs


@library.route("/<string:slug>", methods=["GET"])
@response_model(LibraryDocSchema)
def get_library_doc(slug):
    post = db.first_or_404(
        db.select(DocumentTranslation).filter_by(slug=slug, language=g.locale)
    )
    return post
