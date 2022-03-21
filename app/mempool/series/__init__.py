from flask import Blueprint

bp = Blueprint("series", __name__, url_prefix="/series")

from app.mempool.series import routes  # noqa: E402, F401
