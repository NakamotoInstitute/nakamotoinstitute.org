from flask import Blueprint

bp = Blueprint("podcast", __name__, url_prefix="/podcast")

from app.podcast import routes  # noqa: E402, F401
