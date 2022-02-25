from flask import render_template

from app import cache
from app.satoshi import bp


@bp.route("/")
@cache.cached(key_prefix="satoshi")
def index():
    return render_template("satoshi/index.html")


@bp.route("/code/")
@cache.cached()
def code():
    return render_template("satoshi/code.html")
