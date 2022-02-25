from flask import Blueprint

bp = Blueprint("research", __name__, url_prefix="/research")

from app.research import routes  # noqa: E402, F401
