from flask import Blueprint

bp = Blueprint("literature", __name__, url_prefix="/literature")

from app.literature import routes  # noqa: E402, F401
