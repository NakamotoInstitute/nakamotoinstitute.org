from flask import Blueprint

from app.satoshi.emails import bp as emails_bp

satoshi = Blueprint("satoshi", __name__)
satoshi.register_blueprint(emails_bp)
