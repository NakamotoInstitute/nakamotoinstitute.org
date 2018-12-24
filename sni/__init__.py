#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_caching import Cache
from flask_assets import Environment, Bundle
from flaskext.markdown import Markdown
from flask_flatpages import FlatPages
import jinja2
from datetime import datetime


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ReverseProxied(app.wsgi_app)

# Include docs folder in templates
my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(['sni/templates/',
                             'sni/templates/blog/',
                             'sni/templates/docs/',
                             'sni/templates/podcast/']),
])
app.jinja_loader = my_loader

db = SQLAlchemy(app)

Markdown(app, extensions=['footnotes'])
pages = FlatPages(app)

manager = Manager(app)

# Scss
assets = Environment(app)
assets.url_expire = True
assets.auto_build = True
assets.append_path('sni/assets')
assets.cache = 'sni/assets/.webassets-cache'

scss = Bundle('scss/__main__.scss', filters='pyscss', output='css/main.css',
              depends=['scss/*.scss'])
assets.register('scss_all', scss)

assets.debug = False
app.config['ASSETS_DEBUG'] = False

cache_config = {}
if app.debug:
    cache_config.update({
        'CACHE_TYPE': 'null',
        'CACHE_NO_NULL_WARNING': True,
    })
else:
    cache_config.update({
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache',
        'CACHE_THRESHOLD': 1000,
        'CACHE_DEFAULT_TIMEOUT': 0,
    })

cache = Cache(app, config=cache_config)
with app.app_context():
        cache.clear()

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/snilog.csv',
                                       'a',
                                       10 * 1024 * 1024,
                                       100)

    file_handler.setFormatter(logging.Formatter('%(asctime)s, %(levelname)s, %(message)s'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('sni')


from sni import views, models
from sni.util import filters
