from typing import List

from app import db
from app.models import Author
from app.utils.decorators import response_model

from . import authors
from .schemas import AuthorBaseSchema, AuthorSchema


@authors.route("/", methods=["GET"])
@response_model(List[AuthorBaseSchema])
def get_authors():
    authors = db.session.scalars(db.select(Author)).all()
    return authors


@authors.route("/<string:slug>", methods=["GET"])
@response_model(AuthorSchema)
def get_author(slug):
    author = db.first_or_404(db.select(Author).filter_by(slug=slug))
    return author
