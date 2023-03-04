#
# Satoshi Nakamoto Institute (https://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#
import os

from flask import (
    current_app,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from sqlalchemy import desc

from app import cache, pages
from app.main import bp
from app.models import BlogPost, Doc, Price, ResearchDoc, Skeptic


@bp.route("/favicon.ico")
@bp.route("/favicon.ico", subdomain="satoshi")
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@bp.route("/")
@cache.cached()
def index():
    blog_post = BlogPost.query.order_by(desc(BlogPost.added)).first()
    return render_template("main/index.html", latest_blog_post=blog_post)


@bp.route("/about/", methods=["GET"])
@cache.cached()
def about():
    return render_template("main/about.html")


@bp.route("/contact/", methods=["GET"])
@cache.cached()
def contact():
    return render_template("main/contact.html")


@bp.route("/events/", methods=["GET"])
@cache.cached()
def events():
    return render_template("main/events.html")


@bp.route("/donate/", methods=["GET"])
@cache.cached()
def donate():
    return render_template("main/donate.html")


@bp.route("/<string:slug>/", methods=["GET"])
@cache.cached()
def doc_view(slug):
    doc = Doc.query.filter_by(slug=slug).first()
    if doc is not None:
        formats = [format.name for format in doc.formats]
        if "html" in formats:
            page = pages.get(f"literature/{slug}")
            return render_template(
                "literature/doc.html", doc=doc, page=page, doc_type="literature"
            )
        else:
            return redirect(url_for("literature.detail", slug=slug))
    else:
        doc = ResearchDoc.query.filter_by(slug=slug).first()
        if doc is not None:
            formats = [format.name for format in doc.formats]
            if "html" in formats:
                page = pages.get(f"research/{slug}")
                return render_template(
                    "literature/doc.html", doc=doc, page=page, doc_type="research"
                )
            else:
                return redirect(url_for("research.detail", slug=slug))
    return redirect(url_for("main.index"))


@bp.route("/the-skeptics/")
@cache.cached()
def skeptics():
    skeptics = Skeptic.query.order_by(Skeptic.date).all()
    latest_price = Price.query.all()[-1]
    return render_template(
        "main/the_skeptics.html", skeptics=skeptics, last_updated=latest_price.date
    )


@bp.route("/crash-course/", methods=["GET"])
@cache.cached()
def crash_course():
    return render_template("main/crash-course.html")


# Redirect old links
@bp.route("/<string:url_slug>.<string:ext>/")
@cache.cached()
def reroute(url_slug, ext):
    doc = Doc.query.filter_by(slug=url_slug).first()
    if doc is not None:
        return redirect(url_for("literature.view", slug=doc.slug, ext=ext))
    else:
        doc = ResearchDoc.query.filter_by(slug=url_slug).first()
        if doc is not None:
            return redirect(url_for("research.view", slug=doc.slug, ext=ext))
    return redirect(url_for("main.index"))


@bp.route("/keybase.txt")
@cache.cached()
def keybase():
    return send_from_directory(current_app.static_folder, request.path[1:])
