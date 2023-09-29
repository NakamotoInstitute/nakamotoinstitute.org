from flask import Blueprint

bp = Blueprint("skeptics", __name__)

from . import routes  # noqa F401
