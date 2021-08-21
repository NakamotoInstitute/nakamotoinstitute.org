from flask import Blueprint

bp = Blueprint("quotes", __name__, subdomain="satoshi", url_prefix="/quotes")

from app.satoshi.quotes import routes  # noqa: E402, F401
