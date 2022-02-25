from flask import Blueprint

bp = Blueprint("posts", __name__, subdomain="satoshi", url_prefix="/posts")

from app.satoshi.posts import routes  # noqa: E402, F401
