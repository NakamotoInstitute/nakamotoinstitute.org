from flask import redirect, render_template, url_for

from app import cache
from app.models import ResearchDoc
from app.research import bp


@bp.route("/", methods=["GET"])
@cache.cached()
def index():
    docs = ResearchDoc.query.order_by("id").all()
    formats = {}
    for doc in docs:
        format_names = [doc_format.name for doc_format in doc.formats]
        formats[doc.slug] = format_names
    return render_template("research/index.html", docs=docs, formats=formats)


@bp.route("/<string:slug>/", methods=["GET"])
@cache.cached()
def detail(slug):
    doc = ResearchDoc.query.filter_by(slug=slug).first()
    if doc is not None:
        formats = [doc_format.name for doc_format in doc.formats]
        return render_template(
            "literature/detail.html", doc=doc, formats=formats, is_lit=False
        )
    else:
        return redirect(url_for("research.index"))


@bp.route("/<int:doc_id>/", methods=["GET"])
@cache.cached()
def detail_id(doc_id):
    doc = ResearchDoc.query.filter_by(id=doc_id).first()
    if doc is not None:
        return redirect(url_for("research.detail", slug=doc.slug))
    else:
        return redirect(url_for("research.index"))


@bp.route("/<string:slug>/<string:ext>/", methods=["GET"])
@cache.cached()
def view(slug, ext):
    doc = ResearchDoc.query.filter_by(slug=slug).first()
    if doc is not None:
        formats = [doc_format.name for doc_format in doc.formats]
        if ext in formats:
            if ext == "html":
                return redirect(url_for("main.doc_view", slug=slug))
            else:
                return redirect(url_for("static", filename=f"docs/{slug}.{ext}"))
        else:
            return redirect(url_for("research.detail", slug=slug))
    else:
        return redirect(url_for("research.index"))


@bp.route("/<int:doc_id>/<string:ext>/", methods=["GET"])
@cache.cached()
def view_id(doc_id, ext):
    doc = ResearchDoc.query.filter_by(id=doc_id).first()
    if doc is not None:
        formats = [doc_format.name for doc_format in doc.formats]
        slug = doc.slug
        if ext in formats:
            if ext == "html":
                return redirect(url_for("main.doc_view", slug=slug))
            else:
                return redirect(url_for("static", filename=f"docs/{slug}.{ext}"))
        else:
            return redirect(url_for("research.detail", slug=doc.slug))
    else:
        return redirect(url_for("research.index"))
