#
# Satoshi Nakamoto Institute (https://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import logging
import os
from logging.handlers import RotatingFileHandler

import jinja2
from flask import Flask
from flask_assets import Bundle, Environment
from flask_caching import Cache
from flask_flatpages import FlatPages
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config

db = SQLAlchemy()
pages = FlatPages()
cache = Cache(
    config={
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": "cache",
        "CACHE_DEFAULT_TIMEOUT": 1800,
    }
)

scss = Bundle(
    "scss/main.scss",
    filters="pyscss",
    output="css/main.css",
    depends=["scss/**/*.scss"],
)
assets = Environment()


def register_assets(app):
    assets.init_app(app)
    with app.app_context():
        assets.url_expire = True
        assets.auto_build = True
        assets.append_path("app/assets")
        assets.cache = "app/assets/.webassets-cache"
        assets.debug = False
        assets.register("scss_all", scss)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    template_loader = jinja2.ChoiceLoader(
        [
            app.jinja_loader,
            jinja2.FileSystemLoader(
                [
                    "app/templates/",
                ]
            ),
        ]
    )
    app.jinja_loader = template_loader

    db.init_app(app)
    pages.init_app(app)

    # SCSS
    register_assets(app)

    if app.debug:
        cache.init_app(
            app,
            config={
                "CACHE_TYPE": "null",
                "CACHE_DEFAULT_TIMEOUT": 0,
            },
        )
    else:
        cache.init_app(app)

    from app.authors import bp as authors_bp
    from app.errors import bp as errors_bp
    from app.finney import bp as finney_bp
    from app.literature import bp as literature_bp
    from app.main import bp as main_bp
    from app.mempool import bp as mempool_bp
    from app.podcast import bp as podcast_bp
    from app.research import bp as research_bp
    from app.satoshi import bp as satoshi_bp
    from app.shared import bp as shared_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(satoshi_bp)
    app.register_blueprint(finney_bp)
    app.register_blueprint(literature_bp)
    app.register_blueprint(research_bp)
    app.register_blueprint(mempool_bp)
    app.register_blueprint(podcast_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(shared_bp)

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

    return app
