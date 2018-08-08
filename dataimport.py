#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import json
import datetime
import csv
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
print "Begin deleting Thread"
ts = Thread.query.all()
for t in ts:
    db.session.delete(t)
    db.session.commit()
print "Finish deleting Thread"
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

with open('./data/satoshiemails.json') as data_file:
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

print "Finish importing Email"
print "Begin importing Thread"

with open('data/threads.json') as data_file:
    threads = json.load(data_file)

for thread in threads:
    new_thread = Thread(
        id=thread['id'],
        title=thread['title'],
        url=thread['url'],
        source=thread['source']
    )
    db.session.add(new_thread)
    db.session.commit()

print "Finish importing Thread"
print "Begin importing Post"

with open('data/posts.json') as data_file:
	posts = json.load(data_file)

for i, p in enumerate(posts):

    # quotes = db.relationship("Quote", backref="post")
    # thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    satoshi_id = None
    if 'satoshi_id' in p.keys():
        satoshi_id = p['satoshi_id']
    post = Post(
        id=i+1,
        satoshi_id=satoshi_id,
        url=p['url'],
        subject=p['subject'],
        poster_name=p['name'],
        poster_url=p['poster_url'],
        post_num=p['post_num'],
        is_displayed=p['is_displayed'],
        nested_level=p['nested_level'],
        date=parser.parse(p['date']),
        text=p['content'],
        thread_id=p['thread_id']
    )
    db.session.add(post)
    db.session.commit()

print "Finish importing Post"
print "Begin importing QuoteCategory"

with open('./data/quotecategories.json') as data_file:
	quotecategories = json.load(data_file)

for qc in quotecategories:
	quote_category = QuoteCategory(
		slug=qc['slug'],
		name=qc['name']
	)
	db.session.add(quote_category)
	db.session.commit()

print "Finish importing QuoteCategory"
print "Begin importing Quote"

with open('./data/quotes.json') as data_file:
	quotes = json.load(data_file)

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

with open('./data/authors.json') as data_file:
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

print "Finish importing Author"
print "Begin importing Doc"

with open('./data/literature.json') as data_file:
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

print "Finish importing Doc"
print "Begin importing ResearchDoc"

with open('./data/research.json') as data_file:
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

with open('./data/blogposts.json') as data_file:
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

print "Finish importing ResearchDoc"
print "Begin importing Skeptic"

with open('./data/skeptics.json') as data_file:
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

print "Finish importing Skeptic"
print "Begin importing Episode"

with open('./data/episodes.json') as data_file:
	episodes = json.load(data_file)

for i in range(0,len(episodes)):
	episode = Episode(
		id=episodes[i]['id'],
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
