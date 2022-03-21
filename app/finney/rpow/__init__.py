from flask import Blueprint

bp = Blueprint("rpow", __name__, url_prefix="/rpow")

from app.finney.rpow import routes  # noqa: E402, F401
