from flask import render_template

from app import cache
from app.finney import bp
from app.models import Author


@bp.route("/", methods=["GET"])
@cache.cached()
def index():
    author = Author.query.filter_by(slug="hal-finney").first()
    docs = author.docs.all()
    return render_template("finney/index.html", docs=docs)
