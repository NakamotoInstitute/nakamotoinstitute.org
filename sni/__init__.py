#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.cache import Cache
from flaskext.markdown import Markdown
from flask_flatpages import FlatPages
import jinja2
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')

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
migrate = Migrate(app, db)

Markdown(app, extensions=['footnotes'])
pages = FlatPages(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

from models import DonationAddress


@app.context_processor
def utility_processor():
    def donation_address():
        address = DonationAddress.query.order_by(DonationAddress.lastseen).first()
        if address is None:
            return ''
        address.lastseen = datetime.now()
        db.session.commit()
        address = address.address
        return address
    return dict(donation_address=donation_address)

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
