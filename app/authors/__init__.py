from flask import Blueprint

bp = Blueprint("authors", __name__, url_prefix="/authors")

from app.authors import routes  # noqa: E402, F401
