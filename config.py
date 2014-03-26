#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SERVER_NAME = 'sni:5000'
SQLALCHEMY_DATABASE_URI = "postgresql://[user]:[password]@localhost/[db name]"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DEBUG = False
CSRF_ENABLED = True