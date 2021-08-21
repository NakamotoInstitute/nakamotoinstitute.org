from flask import redirect, render_template, url_for

from app import cache
from app.authors import bp
from app.models import Author


@bp.route("/", methods=["GET"])
@cache.cached()
def index():
    authors = Author.query.order_by(Author.last).all()
    return render_template("authors/index.html", authors=authors)


@bp.route("/<string:slug>/", methods=["GET"])
@cache.cached()
def detail(slug):
    if slug.lower() == "satoshi-nakamoto":
        return redirect(url_for("satoshi.index"))
    author = Author.query.filter_by(slug=slug).first()
    if author is not None:
        mempool_posts = author.blogposts.all()
        literature_docs = author.docs.all()
        research_docs = author.researchdocs.all()
        return render_template(
            "authors/detail.html",
            author=author,
            mempool_posts=mempool_posts,
            literature_docs=literature_docs,
            research_docs=research_docs,
        )
    elif not slug.islower():
        return redirect(url_for("authors.detail", slug=slug.lower()))
    else:
        return redirect(url_for("authors.index"))
