from flask import current_app, render_template

from app import cache
from app.finney.rpow import bp


@bp.route("/", methods=["GET"])
@cache.cached()
def index():
    return render_template("finney/rpow/index.html")


@bp.route("/<path:path>")
@cache.cached()
def site(path):
    return current_app.send_static_file(f"rpow/{path}")
