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
import jinja2


app = Flask(__name__)
app.config.from_object('config')

# Include docs folder in templates
my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(['sni/templates/',
    						 'sni/templates/docs/']),
])
app.jinja_loader = my_loader

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

cache = Cache(app,config={'CACHE_TYPE': 'simple'})

from sni import views, models
