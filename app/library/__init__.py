from flask import Blueprint

library = Blueprint("library", __name__)

from . import routes  # noqa F401
