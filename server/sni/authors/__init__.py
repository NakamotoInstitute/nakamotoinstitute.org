from flask import Blueprint

authors = Blueprint("authors", __name__)

from . import routes  # noqa F401
