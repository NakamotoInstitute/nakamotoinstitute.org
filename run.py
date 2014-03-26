#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

from sni import app, manager
from werkzeug.contrib.fixers import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    manager.run()
