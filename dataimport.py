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
Email.query.delete()
Post.query.delete()
cats = Category.query.all()
for cat in cats:
	db.session.delete(cat)
	db.session.commit()
forms = Format.query.all()
for form in forms:
	db.session.delete(form)
	db.session.commit()
auths = Author.query.all()
for auth in auths:
	db.session.delete(auth)
	db.session.commit()
Doc.query.delete()

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

with open('./literature.json') as data_file:
	docs = json.load(data_file)

for i in range(0, len(docs['docs'])):
	authorlist = docs['docs'][i]['author']
	dbauthor = []
	for auth in authorlist:
		dbauthor += [get_or_create(Author, name=auth)]
	formlist = docs['docs'][i]['formats']
	dbformat = []
	for form in formlist:
		dbformat += [get_or_create(Format, name=form)]
	catlist = docs['docs'][i]['categories']
	dbcat = []
	for cat in catlist:
		dbcat += [get_or_create(Category, name=cat)]
	doc = Doc(
		id=i+1,
		title=docs['docs'][i]['title'],
		author=dbauthor,
		date=docs['docs'][i]['date'],
		slug=docs['docs'][i]['slug'],
		formats=dbformat,
		categories=dbcat,
		doctype=docs['docs'][i]['doctype'])
	db.session.add(doc)
	db.session.commit()

with open('./blogposts.json') as data_file:
	blogps = json.load(data_file)

for i in range(0,len(blogps['blogposts'])):
	blogpost = BlogPost(
		id=i+1,
		title=blogps['blogposts'][i]['title'],
		author=blogps['blogposts'][i]['author'],
		date=parser.parse(blogps['blogposts'][i]['date']),
		slug=blogps['blogposts'][i]['slug'])
	db.session.add(blogpost)
	db.session.commit()