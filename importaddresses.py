#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import csv
from dateutil import parser
from datetime import datetime
from sni.models import DonationAddress
from sni import db

# Clear out database
DonationAddress.query.delete()

# return object

def get(model, **kwargs):
	return db.session.query(model).filter_by(**kwargs).first()

# See if object already exists for uniqueness
def get_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        return instance

with open('./addresses/addresses.csv') as csvfile:
	addresses = csv.reader(csvfile)
	now = datetime.now()
	for address in addresses:
		print address
		record = DonationAddress(address=address[0], lastseen=now)
		db.session.add(record)
		db.session.commit()
