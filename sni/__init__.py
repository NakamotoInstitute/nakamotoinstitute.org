#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import jinja2
from flask_caching import Cache
from flask_flatpages import Environment, Bundle
from flask_flatpages import Flask
from flask_flatpages import FlatPages
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown


class ReverseProxied(object):
    """
    """
    # noinspection PyShadowingNames
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

cache = Cache(app, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache',
    'CACHE_DEFAULT_TIMEOUT': 1800,
})

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    # noinspection PyArgumentEqualDefault
    file_handler = RotatingFileHandler('tmp/snilog.csv',
                                       'a',
                                       10 * 1024 * 1024,
                                       100)

    file_handler.setFormatter(logging.Formatter('%(asctime)s, %(levelname)s, %(message)s'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('sni')

