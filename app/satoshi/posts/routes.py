from flask import redirect, render_template, request, url_for

from app import cache
from app.models import ForumThread, Post
from app.satoshi.posts import bp


@bp.route("/", methods=["GET"])
@cache.cached()
def index():
    posts = Post.query.filter(Post.satoshi_id.isnot(None)).order_by(Post.date).all()
    return render_template("satoshi/posts/index.html", posts=posts)


@bp.route("/threads/", methods=["GET"])
@cache.cached()
def index_threads():
    threads = ForumThread.query.all()
    p2pfoundation_threads = [threads[0]]
    bitcointalk_threads = threads[1:]
    return render_template(
        "satoshi/posts/index_threads.html",
        threads=threads,
        p2pfoundation_threads=p2pfoundation_threads,
        bitcointalk_threads=bitcointalk_threads,
        source=None,
    )


@bp.route("/<string:source>/", methods=["GET"])
@cache.cached()
def index_source(source):
    posts = (
        Post.query.filter(Post.satoshi_id.isnot(None))
        .join(Post.forum_thread)
        .filter_by(source=source)
        .order_by(Post.date)
        .all()
    )
    if len(posts) != 0:
        return render_template("satoshi/posts/index.html", posts=posts, source=source)
    else:
        return redirect(url_for("satoshi.posts.index"))


@bp.route("/<string:source>/<int:post_id>/", methods=["GET"])
@cache.cached()
def detail(source, post_id):
    post = (
        Post.query.filter_by(satoshi_id=post_id)
        .join(Post.forum_thread)
        .filter_by(source=source)
        .first()
    )
    previous_post = (
        Post.query.filter_by(satoshi_id=post_id - 1).join(Post.forum_thread).first()
    )
    next_post = (
        Post.query.filter_by(satoshi_id=post_id + 1).join(Post.forum_thread).first()
    )
    if post is not None:
        return render_template(
            "satoshi/posts/detail.html",
            post=post,
            previous_post=previous_post,
            next_post=next_post,
        )
    else:
        return redirect("posts")


@bp.route("/<string:source>/threads/", methods=["GET"])
@cache.cached()
def threads(source):
    threads = ForumThread.query.filter_by(source=source).order_by(ForumThread.id).all()
    if len(threads) != 0:
        return render_template(
            "satoshi/posts/index_threads.html", threads=threads, source=source
        )
    else:
        return redirect(url_for("satoshi.posts.index", view="threads"))


@bp.route(
    "/<string:source>/threads/<int:thread_id>/",
    methods=["GET"],
)
@cache.cached()
def detail_thread(source, thread_id):
    view_query = request.args.get("view")
    posts = Post.query.filter_by(thread_id=thread_id)
    if len(posts.all()) > 0:
        thread = posts[0].forum_thread
        if thread.source != source:
            return redirect(
                url_for(
                    "satoshi.posts.detail_thread",
                    source=thread.source,
                    thread_id=thread_id,
                )
            )
    else:
        return redirect(url_for("satoshi.posts.index", view="threads"))
    if view_query == "satoshi":
        posts = posts.filter(Post.satoshi_id.isnot(None))
    posts = posts.all()
    previous_thread = ForumThread.query.filter_by(id=thread_id - 1).first()
    next_thread = ForumThread.query.filter_by(id=thread_id + 1).first()
    return render_template(
        "satoshi/posts/detail_thread.html",
        posts=posts,
        previous_thread=previous_thread,
        next_thread=next_thread,
    )
