from flask import Blueprint

bp = Blueprint("podcast", __name__)

from . import routes  # noqa F401
