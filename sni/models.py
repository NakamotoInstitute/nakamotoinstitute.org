#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

from sni import db, app


class Email(db.Model):
 	id = db.Column(db.Integer, primary_key = True)
 	subject = db.Column(db.String())
 	sent_from = db.Column(db.String())
 	date = db.Column(db.DateTime)
 	text = db.Column(db.String())
 	source = db.Column(db.String())

 	def __repr__(self):
 		return '<Email %r>' % (self.subject)

class Post(db.Model):
 	id = db.Column(db.Integer, primary_key = True)
 	url = db.Column(db.String())
 	name = db.Column(db.String())
 	date = db.Column(db.DateTime)
 	text = db.Column(db.String())
 	source = db.Column(db.String())

 	def __repr__(self):
 		return '<Post %r>' % (self.name)

authors = db.Table('authors',
	db.Column('doc_id', db.Integer, db.ForeignKey('doc.id')),
	db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)

class Author(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String())

	def __repr__(self):
 		return '<Author %r>' % (self.name)

formats = db.Table('formats',
	db.Column('doc_id', db.Integer, db.ForeignKey('doc.id')),
	db.Column('format_id', db.Integer, db.ForeignKey('format.id'))
)

class Format(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String())

	def __repr__(self):
 		return '<Format %r>' % (self.name)

categories = db.Table('categories',
	db.Column('doc_id', db.Integer, db.ForeignKey('doc.id')),
	db.Column('category_id', db.Integer, db.ForeignKey('category.id')))

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String())

	def __repr__(self):
 		return '<Category %r>' % (self.name)

class Doc(db.Model):
 	id = db.Column(db.Integer, primary_key = True)
 	title = db.Column(db.String())
 	author = db.relationship('Author',
 		secondary = authors,
 		backref=db.backref('docs', lazy='dynamic'))
 	date = db.Column(db.String())
 	slug = db.Column(db.String())
 	formats = db.relationship('Format',
 		secondary = formats,
 		backref=db.backref('docs', lazy='dynamic'))
 	categories = db.relationship('Category',
 		secondary = categories,
 		backref=db.backref('docs', lazy='dynamic'))
 	doctype = db.Column(db.String())

 	def __repr__(self):
 		return '<Doc %r>' % (self.title)

