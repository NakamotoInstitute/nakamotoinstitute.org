#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import datetime
import csv
import yaml
from dateutil import parser
from datetime import datetime
from sni.models import *

# Clear out database
print "Begin deleting Quote"
qs = Quote.query.all()
for q in qs:
    db.session.delete(q)
    db.session.commit()
print "Finish deleting Quote"
print "Begin deleting QuoteCategory"
qcs = QuoteCategory.query.all()
for qc in qcs:
    db.session.delete(qc)
    db.session.commit()
print "Finish deleting QuoteCategory"
print "Begin deleting Email"
Email.query.delete()
print "Finish deleting Email"
print "Begin deleting Post"
Post.query.delete()
print "Finish deleting Post"
print "Begin deleting Category"
cats = Category.query.all()
for cat in cats:
	db.session.delete(cat)
	db.session.commit()
print "Finish deleting Category"
print "Begin deleting Format"
forms = Format.query.all()
for form in forms:
	db.session.delete(form)
	db.session.commit()
print "Finish deleting Format"
print "Begin deleting Author"
auths = Author.query.all()
for auth in auths:
	db.session.delete(auth)
	db.session.commit()
print "Finish deleting Author"
print "Begin deleting Doc"
Doc.query.delete()
print "Finish deleting Doc"
print "Begin deleting ResearchDoc"
ResearchDoc.query.delete()
print "Finish deleting ResearchDoc"
print "Begin deleting BlogPost"
BlogPost.query.delete()
print "Finish deleting BlogPost"
print "Begin deleting Skeptic"
Skeptic.query.delete()
print "Finish deleting Skeptic"
print "Begin deleting Episode"
Episode.query.delete()
print "Finish deleting Episode"

#db.drop_all()
#db.create_all()

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

print "Begin importing Email"

with open('./data/satoshiemails.yaml') as data_file:
    try:
    	emails = yaml.load(data_file)
    except yaml.YAMLError as exc:
        print(exc)

for i in range(0,len(emails)):
	index = len(emails)-1-i
	email = Email(
		id=i+1,
		subject=emails[index]['Subject'],
		sent_from=emails[index]['From'],
		date=parser.parse(emails[index]['Date']),
		text=emails[index]['Text'],
		source=emails[index]['Source'])
	db.session.add(email)
	db.session.commit()

print "Finish importing Email"
print "Begin importing Post"

with open('./data/satoshiposts.yaml') as data_file:
    try:
    	posts = yaml.load(data_file)
    except yaml.YAMLError as exc:
        print(exc)

for i in range(0,len(posts)):
	index = len(posts)-1-i
	post = Post(
		id=i+1,
		url=posts[index]['url'],
		name=posts[index]['name'],
		date=parser.parse(posts[index]['date']),
		text=posts[index]['post'],
		source=posts[index]['source'])
	db.session.add(post)
	db.session.commit()

print "Finish importing Post"
print "Begin importing QuoteCategory"

with open('./data/quotecategories.yaml') as data_file:
    try:
    	quotecategories = yaml.load(data_file)
    except yaml.YAMLError as exc:
        print(exc)

for qc in quotecategories:
	quote_category = QuoteCategory(
		slug=qc['slug'],
		name=qc['name']
	)
	db.session.add(quote_category)
	db.session.commit()

print "Finish importing QuoteCategory"
print "Begin importing Quote"

with open('./data/quotes.yaml') as data_file:
    try:
    	quotes = yaml.load(data_file)
    except yam{l.YAMLError as exc:
        print(exc)

for i, quote in enumerate(quotes):
	q = Quote(
		id = i+1,
		text=quote['text'],
	    date=parser.parse(quote['date']).date(),
	    medium=quote['medium']
	)
	if 'email_id' in quote:
		q.email_id = quote['email_id']
	if 'post_id' in quote:
		q.post_id = quote['post_id']
	categories = []
	for cat in quote['category'].split(', '):
		categories += [get(QuoteCategory, slug=cat)]
	q.categories = categories
	db.session.add(q)
	db.session.commit()

print "Finish importing Quote"
print "Begin importing Author"

with open('./data/authors.yaml') as data_file:
    try:
    	authors = yaml.load(data_file)
    except yaml.YAMLError as exc:
        print(exc)

for i in range(0, len(authors)):
	author = Author(
		id=i+1,
		first=authors[i]['first'],
		middle=authors[i]['middle'],
		last=authors[i]['last'],
		slug=authors[i]['slug'])
	db.session.add(author)
	db.session.commit()

print "Finish importing Author"
print "Begin importing Doc"

with open('./data/literature.yaml') as data_file:
    try:
    	docs = yaml.load(data_file)
    except yaml.YAMLError as exc:
        print(exc)

for i in range(0, len(docs)):
	authorlist = docs[i]['author']
	dbauthor = []
	for auth in authorlist:
		dbauthor += [get(Author, slug=auth)]
	formlist = docs[i]['formats']
	dbformat = []
	for form in formlist:
		dbformat += [get_or_create(Format, name=form)]
	catlist = docs[i]['categories']
	dbcat = []
	for cat in catlist:
		dbcat += [get_or_create(Category, name=cat)]
	if 'external' in docs[i]:
		ext = docs[i]['external']
	else:
		ext = None
	doc = Doc(
		id=docs[i]['id'],
		title=docs[i]['title'],
		author=dbauthor,
		date=docs[i]['date'],
		slug=docs[i]['slug'],
		formats=dbformat,
		categories=dbcat,
		doctype=docs[i]['doctype'],
		external=ext)
	db.session.add(doc)
	db.session.commit()

print "Finish importing Doc"
print "Begin importing ResearchDoc"

with open('./data/research.yaml') as data_file:
    try:
    	research = yaml.load(data_file)
    except yaml.YAMLError as exc:
        print(exc)

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
	if 'external' in research[i]:
		ext = research[i]['external']
	else:
		ext = None
	if 'lit_id' in research[i]:
		lit = research[i]['lit_id']
	else:
		lit_id = None
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
		lit_id=lit)
	db.session.add(doc)
	db.session.commit()

print "Finish importing ResearchDoc"
print "Begin importing BlogPost"

with open('./data/blogposts.yaml') as data_file:
    try:
    	blogps = yaml.load(data_file)
    except yaml.YAMLError as exc:
        print(exc)

for i in range(0,len(blogps)):
	blogpost = BlogPost(
		id=i+1,
		title=blogps[i]['title'],
		author=[get(Author,slug=blogps[i]['author'])],
		date=parser.parse(blogps[i]['date']),
		added=parser.parse(blogps[i]['added']),
		slug=blogps[i]['slug'],
		excerpt=blogps[i]['excerpt'],
		languages=blogps[i]['languages'])
	db.session.add(blogpost)
	db.session.commit()

print "Finish importing ResearchDoc"
print "Begin importing Skeptic"

with open('./data/skeptics.yaml') as data_file:
    try:
    	skeptics = yaml.load(data_file)
    except yaml.YAMLError as exc:
        print(exc)

for i in range(0,len(skeptics)):
	skeptic = Skeptic(
		id = i + 1,
		name = skeptics[i]['name'],
		title = skeptics[i]['title'],
		article = skeptics[i]['article'],
		date = parser.parse(skeptics[i]['date']),
		source = skeptics[i]['source'],
		excerpt = skeptics[i]['excerpt'],
		price = skeptics[i]['price'],
		link = skeptics[i]['link'],
		waybacklink = skeptics[i]['waybacklink'],
		slug = skeptics[i]['slug']+'-'+str(parser.parse(skeptics[i]['date']))[0:10])
	db.session.add(skeptic)
	db.session.commit()

print "Finish importing Skeptic"
print "Begin importing Episode"

with open('./data/episodes.yaml') as data_file:
    try:
    	episodes = yaml.load(data_file)
    except yaml.YAMLError as exc:
        print(exc)

for i in range(0,len(episodes)):
	episode = Episode(
		title=episodes[i]['title'],
		date=parser.parse(episodes[i]['date']),
		duration=episodes[i]['duration'],
		subtitle=episodes[i]['subtitle'],
		summary=episodes[i]['summary'],
		slug=episodes[i]['slug'],
		youtube=episodes[i]['youtube'],
		address=episodes[i]['address'],
		time=parser.parse(episodes[i]['time']))
	db.session.add(episode)
	db.session.commit()

print "Finish importing Episode"

#with open('./data/addresses/addresses.csv') as csvfile:
#	addresses = csv.reader(csvfile)
#	now = datetime.now()
#	for address in addresses:
#		record = DonationAddress(address=address[0], lastseen=now)
#		db.session.add(record)
#		db.session.commit()
