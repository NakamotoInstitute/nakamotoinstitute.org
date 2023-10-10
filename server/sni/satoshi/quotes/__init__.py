from flask import Blueprint

bp = Blueprint("quotes", __name__, url_prefix="/quotes")

from . import routes  # noqa: E402, F401
