from flask import redirect, render_template, url_for
from sqlalchemy import desc

from app import cache
from app.mempool.series import bp
from app.models import BlogSeries


@bp.route("/")
@cache.cached()
def index():
    series = BlogSeries.query.order_by(desc(BlogSeries.id)).all()
    return render_template("mempool/series/index.html", series=series)


@bp.route("/<string:slug>/")
@cache.cached()
def detail(slug):
    series = BlogSeries.query.filter_by(slug=slug).first()
    if series:
        return render_template("mempool/series/detail.html", series=series)
    else:
        return redirect(url_for("mempool.series.index"))
