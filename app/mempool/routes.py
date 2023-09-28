from typing import List

from flask import g, jsonify

from app import db
from app.models import BlogPost, BlogPostTranslation, BlogSeries, BlogSeriesTranslation
from app.utils.decorators import response_model

from . import mempool
from .schemas import MempoolPostSchema, MempoolSeriesResponse, MempoolSeriesSchema


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


@mempool.route("/latest", methods=["GET"])
@response_model(MempoolPostSchema)
def get_latest_mempool_post():
    post = db.first_or_404(
        db.select(BlogPostTranslation)
        .filter_by(language=g.locale)
        .join(BlogPost)
        .order_by(BlogPost.added.desc())
    )
    return post


@mempool.route("/series", methods=["GET"])
@response_model(List[MempoolSeriesSchema])
def get_all_mempool_series():
    series = db.session.scalars(
        db.select(BlogSeriesTranslation)
        .join(BlogSeries)
        .filter(BlogSeriesTranslation.language == g.locale)
    ).all()
    return series


@mempool.route("/series/<string:slug>", methods=["GET"])
def get_mempool_series(slug):
    series = db.first_or_404(
        db.select(BlogSeriesTranslation).filter_by(slug=slug, language=g.locale)
    )

    posts = db.session.scalars(
        db.select(BlogPostTranslation)
        .join(BlogPost)
        .join(BlogSeries)
        .filter(BlogPostTranslation.language == g.locale, BlogSeries.id == series.id)
    ).all()

    response_data = MempoolSeriesResponse(series=series, posts=posts)

    return jsonify(response_data.dict())
