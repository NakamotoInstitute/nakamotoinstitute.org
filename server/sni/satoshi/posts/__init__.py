from flask import Blueprint

bp = Blueprint("posts", __name__, url_prefix="/posts")

from . import routes  # noqa: E402, F401
