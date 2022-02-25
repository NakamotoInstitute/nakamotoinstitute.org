from flask import Blueprint

bp = Blueprint("emails", __name__, subdomain="satoshi", url_prefix="/emails")

from app.satoshi.emails import routes  # noqa: E402, F401
