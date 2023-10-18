import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, g, redirect, request
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from sni import cli
from sni.extensions import cache, db
from sni.models import blog_post_authors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    register_configurations(app)
    register_extensions(app)
    apply_app_decorators(app)
    register_errorhandlers(app)
    register_blueprints(app)
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

    prod_cache_config = {
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": "cache",
        "CACHE_DEFAULT_TIMEOUT": 1800,
    }

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
    from sni.errors import bp as errors_bp

    app.register_blueprint(errors_bp)


def register_blueprints(app):
    from sni.authors import authors as authors_bp
    from sni.library import library as library_bp
    from sni.mempool import mempool as mempool_bp
    from sni.podcast import bp as podcast_bp
    from sni.satoshi import satoshi as satoshi_bp
    from sni.skeptics import bp as skeptics_bp

    app.register_blueprint(satoshi_bp, url_prefix="/satoshi")
    app.register_blueprint(authors_bp, url_prefix="/authors")
    app.register_blueprint(library_bp, url_prefix="/library")
    app.register_blueprint(mempool_bp, url_prefix="/mempool")
    app.register_blueprint(skeptics_bp, url_prefix="/skeptics")
    app.register_blueprint(podcast_bp, url_prefix="/podcast")


def register_shellcontext(app):
    def shell_context():
        return {"blog_post_authors": blog_post_authors}

    app.shell_context_processor(shell_context)


def register_cli(app):
    cli.register(app)


def register_logger(app):
    if not app.debug:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/sni.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("SNI startup")
