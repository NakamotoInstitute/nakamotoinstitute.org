import logging
import sys

from flask import Flask, g, redirect, request
from werkzeug.middleware.proxy_fix import ProxyFix

from sni import authors, cli, errors, library, mempool, podcast, satoshi, skeptics
from sni.config import Config
from sni.extensions import cache, db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    register_configurations(app)
    register_extensions(app)
    apply_app_decorators(app)
    register_errorhandlers(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_cli(app)
    register_logger(app)
    return app


def register_configurations(app):
    app.url_map.strict_slashes = False
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


def register_extensions(app):
    db.init_app(app)

    debug_cache_config = {
        "CACHE_TYPE": "null",
        "CACHE_DEFAULT_TIMEOUT": 0,
    }
    prod_cache_config = debug_cache_config

    cache_config = debug_cache_config if app.debug else prod_cache_config
    cache.init_app(app, config=cache_config)


def apply_app_decorators(app):
    @app.before_request
    def remove_trailing_slash():
        if request.path != "/" and request.path.endswith("/"):
            return redirect(request.path[:-1])

    @app.url_value_preprocessor
    def set_locale(endpoint, values):
        g.locale = request.args.get("locale", "en")


def register_errorhandlers(app):
    app.register_blueprint(errors.handlers.blueprint)


def register_blueprints(app):
    app.register_blueprint(satoshi.routes.blueprint)
    app.register_blueprint(authors.routes.blueprint)
    app.register_blueprint(library.routes.blueprint)
    app.register_blueprint(mempool.routes.blueprint)
    app.register_blueprint(skeptics.routes.blueprint)
    app.register_blueprint(podcast.routes.blueprint)


def register_shellcontext(app):
    app.shell_context_processor(cli.context.make_shell_context)


def register_cli(app):
    app.register_blueprint(cli.data.blueprint)


def register_logger(app):
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
