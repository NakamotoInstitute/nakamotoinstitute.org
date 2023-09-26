from typing import List

from flask import g

from app import db
from app.models import BlogPost, BlogPostTranslation
from app.utils.decorators import response_model

from . import mempool
from .schemas import MempoolPostSchema


@mempool.route("/", methods=["GET"])
@response_model(List[MempoolPostSchema])
def get_mempool_posts():
    posts = db.session.scalars(
        db.select(BlogPostTranslation)
        .join(BlogPost)
        .filter(BlogPostTranslation.language == g.locale)
        .order_by(BlogPost.added.desc())
    ).all()
    return posts


@mempool.route("/<string:slug>", methods=["GET"])
@response_model(MempoolPostSchema)
def get_mempool_post(slug):
    post = db.first_or_404(
        db.select(BlogPostTranslation).filter_by(slug=slug, language=g.locale)
    )
    return post
