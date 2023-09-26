from typing import List

from flask import g, jsonify

from app import db
from app.models import Author, BlogPost, BlogPostTranslation
from app.utils.decorators import response_model

from . import authors
from .schemas import AuthorResponse, AuthorSchema


@authors.route("/", methods=["GET"])
@response_model(List[AuthorSchema])
def get_authors():
    authors = db.session.scalars(db.select(Author)).all()
    return authors


@authors.route("/<string:slug>", methods=["GET"])
def get_author(slug):
    author = db.first_or_404(db.select(Author).filter_by(slug=slug))
    mempool_posts = db.session.scalars(
        db.select(BlogPostTranslation)
        .join(BlogPost)
        .join(Author)
        .filter(Author.id == author.id, BlogPostTranslation.language == g.locale)
    ).all()
    response_data = AuthorResponse(author=author, mempool=mempool_posts)

    return jsonify(response_data.dict())
