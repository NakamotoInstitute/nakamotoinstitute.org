from typing import List

from flask import Blueprint, jsonify

from sni.extensions import db
from sni.satoshi.posts.models import ForumPost, ForumThread
from sni.utils.decorators import response_model
from sni.utils.request import get_bool_param

from .schemas import (
    ForumPostBaseModel,
    ForumPostDetailModel,
    ForumPostModel,
    ForumThreadBaseModel,
    ForumThreadModel,
)

blueprint = Blueprint("posts", __name__, url_prefix="/posts")


@blueprint.route("/", methods=["GET"])
@response_model(List[ForumPostBaseModel])
def get_forum_posts():
    posts = db.session.scalars(
        db.select(ForumPost)
        .filter(ForumPost.satoshi_id.isnot(None))
        .order_by(ForumPost.date)
    ).all()
    return posts


@blueprint.route("/threads", methods=["GET"])
@response_model(List[ForumThreadBaseModel])
def get_forum_threads():
    threads = db.session.scalars(db.select(ForumThread)).all()
    return threads


@blueprint.route("/<string:source>", methods=["GET"])
@response_model(List[ForumPostModel])
def get_forum_posts_by_source(source):
    posts = db.session.scalars(
        db.select(ForumPost)
        .filter(ForumPost.satoshi_id.isnot(None))
        .join(ForumThread)
        .filter_by(source=source)
        .order_by(ForumPost.date)
    ).all()
    return posts


@blueprint.route("/<string:source>/<int:satoshi_id>", methods=["GET"])
def get_forum_post_by_source(source, satoshi_id):
    post = db.first_or_404(
        db.select(ForumPost)
        .filter_by(satoshi_id=satoshi_id)
        .join(ForumThread)
        .filter_by(source=source)
    )
    previous_post = db.session.scalar(
        db.select(ForumPost).filter_by(satoshi_id=satoshi_id - 1).join(ForumThread)
    )
    next_post = db.session.scalar(
        db.select(ForumPost).filter_by(satoshi_id=satoshi_id + 1).join(ForumThread)
    )

    response_data = ForumPostDetailModel(
        post=post, previous=previous_post, next=next_post
    )

    return jsonify(response_data.dict(by_alias=True))


@blueprint.route("/<string:source>/threads", methods=["GET"])
@response_model(List[ForumThreadBaseModel])
def get_forum_threads_by_source(source):
    threads = db.session.scalars(
        db.select(ForumThread).filter_by(source=source).order_by(ForumThread.id)
    ).all()
    return threads


@blueprint.route("/<string:source>/threads/<int:thread_id>", methods=["GET"])
def get_forum_thread_by_source(source, thread_id):
    satoshi_only = get_bool_param("satoshi")

    posts_query = (
        db.select(ForumPost)
        .join(ForumThread)
        .filter(ForumPost.thread_id == thread_id, ForumThread.source == source)
    )
    if satoshi_only:
        posts_query = posts_query.filter(ForumPost.satoshi_id.isnot(None))
    posts = db.session.scalars(posts_query).all()

    thread = posts[0].thread

    previous_thread = db.session.scalar(
        db.select(ForumThread).filter_by(id=thread_id - 1)
    )
    next_thread = db.session.scalar(db.select(ForumThread).filter_by(id=thread_id + 1))

    response_data = ForumThreadModel(
        posts=posts, thread=thread, previous=previous_thread, next=next_thread
    )

    return jsonify(response_data.dict(by_alias=True))
