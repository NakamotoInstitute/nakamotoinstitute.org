from flask import Blueprint

from sni.satoshi import emails, posts, quotes

blueprint = Blueprint("satoshi", __name__, url_prefix="/satoshi")

blueprint.register_blueprint(emails.routes.blueprint)
blueprint.register_blueprint(posts.routes.blueprint)
blueprint.register_blueprint(quotes.routes.blueprint)
