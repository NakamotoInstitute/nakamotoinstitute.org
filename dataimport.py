#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import json
import datetime
from dateutil import parser
from sni.models import *

# Clear out database
# Email.query.delete()
# Post.query.delete()
# cats = Category.query.all()
# for cat in cats:
# 	db.session.delete(cat)
# 	db.session.commit()
# forms = Format.query.all()
# for form in forms:
# 	db.session.delete(form)
# 	db.session.commit()
# auths = Author.query.all()
# for auth in auths:
# 	db.session.delete(auth)
# 	db.session.commit()
# Doc.query.delete()
# ResearchDoc.query.delete()
# BlogPost.query.delete()
# Skeptic.query.delete()

db.drop_all()
db.create_all()

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

with open('./satoshiemails.json') as data_file:
	emails = json.load(data_file)

for i in range(0,len(emails['emails'])):
	index = len(emails['emails'])-1-i
	email = Email(
		id=i+1,
		subject=emails['emails'][index]['Subject'],
		sent_from=emails['emails'][index]['From'],
		date=parser.parse(emails['emails'][index]['Date']),
		text=emails['emails'][index]['Text'],
		source=emails['emails'][index]['Source'])
	db.session.add(email)
	db.session.commit()

with open('./satoshiposts.json') as data_file:
	posts = json.load(data_file)

for i in range(0,len(posts['posts'])):
	index = len(posts['posts'])-1-i
	post = Post(
		id=i+1,
		url=posts['posts'][index]['url'],
		name=posts['posts'][index]['name'],
		date=parser.parse(posts['posts'][index]['date']),
		text=posts['posts'][index]['post'],
		source=posts['posts'][index]['source'])
	db.session.add(post)
	db.session.commit()

with open('./authors.json') as data_file:
	authors = json.load(data_file)

for i in range(0, len(authors['authors'])):
	author = Author(
		id=i+1,
		first=authors['authors'][i]['first'],
		middle=authors['authors'][i]['middle'],
		last=authors['authors'][i]['last'],
		slug=authors['authors'][i]['slug'])
	db.session.add(author)
	db.session.commit()

with open('./literature.json') as data_file:
	docs = json.load(data_file)

for i in range(0, len(docs['docs'])):
	authorlist = docs['docs'][i]['author']
	dbauthor = []
	for auth in authorlist:
		dbauthor += [get(Author, slug=auth)]
	formlist = docs['docs'][i]['formats']
	dbformat = []
	for form in formlist:
		dbformat += [get_or_create(Format, name=form)]
	catlist = docs['docs'][i]['categories']
	dbcat = []
	for cat in catlist:
		dbcat += [get_or_create(Category, name=cat)]
	if 'external' in docs['docs'][i]:
		ext = docs['docs'][i]['external']
	else:
		ext = None
	doc = Doc(
		id=docs['docs'][i]['id'],
		title=docs['docs'][i]['title'],
		author=dbauthor,
		date=docs['docs'][i]['date'],
		slug=docs['docs'][i]['slug'],
		formats=dbformat,
		categories=dbcat,
		doctype=docs['docs'][i]['doctype'],
		external=ext)
	db.session.add(doc)
	db.session.commit()

with open('./research.json') as data_file:
	research = json.load(data_file)

for i in range(0, len(research)):
	authorlist = research[i]['author']
	dbauthor = []
	for auth in authorlist:
		dbauthor += [get(Author, slug=auth)]
	formlist = research[i]['formats']
	dbformat = []
	for form in formlist:
		dbformat += [get_or_create(Format, name=form)]
	catlist = research[i]['categories']
	dbcat = []
	for cat in catlist:
		dbcat += [get_or_create(Category, name=cat)]
	if 'external' in docs['docs'][i]:
		ext = docs['docs'][i]['external']
	else:
		ext = None
	doc = ResearchDoc(
		id=research[i]['id'],
		title=research[i]['title'],
		author=dbauthor,
		date=research[i]['date'],
		slug=research[i]['slug'],
		formats=dbformat,
		categories=dbcat,
		doctype=research[i]['doctype'],
		external=ext,
		lit_id=research[i]['lit_id'])
	db.session.add(doc)
	db.session.commit()

with open('./blogposts.json') as data_file:
	blogps = json.load(data_file)

for i in range(0,len(blogps['blogposts'])):
	blogpost = BlogPost(
		id=i+1,
		title=blogps['blogposts'][i]['title'],
		author=[get(Author,slug=blogps['blogposts'][i]['author'])],
		date=parser.parse(blogps['blogposts'][i]['date']),
		added=parser.parse(blogps['blogposts'][i]['added']),
		slug=blogps['blogposts'][i]['slug'],
		excerpt=blogps['blogposts'][i]['excerpt'],
		languages=blogps['blogposts'][i]['languages'])
	db.session.add(blogpost)
	db.session.commit()

with open('./skeptics.json') as data_file:
	skeptics = json.load(data_file)

for i in range(0,len(skeptics['skeptics'])):
	skeptic = Skeptic(
		id = i + 1,
		name = skeptics['skeptics'][i]['name'],
		title = skeptics['skeptics'][i]['title'],
		article = skeptics['skeptics'][i]['article'],
		date = parser.parse(skeptics['skeptics'][i]['date']),
		source = skeptics['skeptics'][i]['source'],
		excerpt = skeptics['skeptics'][i]['excerpt'],
		price = skeptics['skeptics'][i]['price'],
		link = skeptics['skeptics'][i]['link'],
		waybacklink = skeptics['skeptics'][i]['waybacklink'],
		slug = skeptics['skeptics'][i]['slug']+'-'+str(parser.parse(skeptics['skeptics'][i]['date']))[0:10])
	db.session.add(skeptic)
	db.session.commit()

with open('./addresses/addresses.csv') as csvfile:
	addresses = csv.reader(csvfile)
	now = datetime.now()
	for address in addresses:
		record = DonationAddress(address=address[0], lastseen=now)
		db.session.add(record)
		db.session.commit()