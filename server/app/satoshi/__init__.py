from flask import Blueprint

from app.satoshi.emails import bp as emails_bp
from app.satoshi.posts import bp as forum_posts_bp
from app.satoshi.quotes import bp as quotes_bp

satoshi = Blueprint("satoshi", __name__)
satoshi.register_blueprint(emails_bp)
satoshi.register_blueprint(forum_posts_bp)
satoshi.register_blueprint(quotes_bp)
