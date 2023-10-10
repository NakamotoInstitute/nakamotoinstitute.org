from flask import Blueprint

bp = Blueprint("emails", __name__, url_prefix="/emails")

from . import routes  # noqa: E402, F401
