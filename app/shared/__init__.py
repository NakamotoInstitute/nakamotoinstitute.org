from flask import Blueprint

bp = Blueprint("shared", __name__)

from app.shared import filters  # noqa: E402, F401
