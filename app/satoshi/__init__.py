from flask import Blueprint

from app.satoshi.emails import bp as emails_bp
from app.satoshi.posts import bp as posts_bp
from app.satoshi.quotes import bp as quotes_bp

bp = Blueprint("satoshi", __name__, subdomain="satoshi")
bp.register_blueprint(posts_bp)
bp.register_blueprint(emails_bp)
bp.register_blueprint(quotes_bp)

from app.satoshi import routes  # noqa: E402, F401
