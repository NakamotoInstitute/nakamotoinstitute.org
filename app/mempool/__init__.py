from flask import Blueprint

mempool = Blueprint("mempool", __name__)

from . import routes  # noqa F401
