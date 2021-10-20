#
# Satoshi Nakamoto Institute (http://nakamotoinstitute.org)
# Copyright 2013 Satoshi Nakamoto Institute
# Licensed under GNU Affero GPL (https://github.com/pierrerochard/SNI-private/blob/master/LICENSE)
#

import unittest

from config import SERVER_NAME

from sni import app


class TestCase(unittest.TestCase):
	#Test Homepages
	def test_index(self):
		tester = app.test_client(self)
		resp = tester.get('/').data
		assert "I've been working on" in resp
		#Test
		resp = tester.get('http://satoshi.'+SERVER_NAME).data
		assert "Emails" and "Forum Posts" and "Code" in resp

	#Test About Page
	def test_about(self):
		tester = app.test_client(self)
		resp = tester.get('/about').data
		assert "Redirecting..." in resp
		resp = tester.get('/about/').data
		assert "The Satoshi Nakamoto Institute (SNI) was founded in November 2013" in resp

	#Test Contact Page
	def test_contact(self):
		tester = app.test_client(self)
		resp = tester.get('/contact').data
		assert "Redirecting..." in resp
		resp = tester.get('/contact/').data
		assert "contact (at) nakamotoinstitute.org" in resp

	#Test Email Index
	def test_emails(self):
		tester = app.test_client(self)
		resp = tester.get('/emails/').data
		assert "Page Not Found" in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/emails').data
		assert "Redirecting..." in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/emails/').data
		assert "Cryptography Mailing List Emails" in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/emails/cryptography').data
		assert "Redirecting..." in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/emails/cryptography/').data
		assert "Cryptography Mailing List Emails" in resp

	#Test Email View
	def test_emailview(self):
		tester = app.test_client(self)
		resp = tester.get('/emails/1').data
		assert "Page Not Found" in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/emails/1/').data
		assert "Page Not Found" in resp
		#Test real email
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/emails/cryptography/1').data
		assert "Redirecting..." in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/emails/cryptography/1/').data
		assert "The Cryptography Mailing List" in resp
		#Test non-existing email
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/emails/cryptography/19').data
		assert "Redirecting..." in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/emails/cryptography/19/').data
		assert "Redirecting..." in resp # Goes back to index

	#Test Post Index
	def test_posts(self):
		tester = app.test_client(self)
		resp = tester.get('/posts/').data
		assert "Page Not Found" in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/posts').data
		assert "Redirecting..." in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/posts/').data
		assert "Forum Posts" in resp

	#Test Post View
	def test_postview(self):
		tester = app.test_client(self)
		resp = tester.get('/emails/1').data
		assert "Page Not Found" in resp
		#Test real post
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/posts/1').data
		assert "Redirecting..." in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/posts/1/').data
		assert "Original Post" in resp
		#Test non-existing post
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/posts/1000').data
		assert "Redirecting..." in resp
		resp = tester.get('http://satoshi.'+SERVER_NAME+'/posts/1000/').data
		assert "Redirecting..." in resp # Goes back to index

	#Test Literature index
	def test_literature(self):
		tester = app.test_client(self)
		resp = tester.get('/literature').data
		assert "Redirecting..." in resp
		resp = tester.get('/literature/').data
		assert "Literature" in resp

	#Test document info page
	def test_docinfo(self):
		tester = app.test_client(self)
		#Test real doc
		resp = tester.get('/literature/1').data
		assert "Redirecting..." in resp
		resp = tester.get('/literature/1/').data
		assert "Date:" and "Formats:" in resp
		#Test non-existing doc
		resp = tester.get('/literature/1000').data
		assert "Redirecting..." in resp
		resp = tester.get('/literature/1000/').data
		assert "Redirecting..." in resp

	#Test document view page
	def test_docview(self):
		tester = app.test_client(self)
		#Test real doc format
		resp = tester.get('/literature/1/html').data
		assert "Redirecting..." in resp
		resp = tester.get('/literature/1/html/').data
		assert "A purely peer-to-peer version of electronic cash would allow" in resp
		#Test real doc format in static files
		resp = tester.get('/literature/1/pdf').data
		assert "Redirecting..." in resp
		resp = tester.get('/literature/1/pdf/').data
		assert "Redirecting..." in resp
		#Test fake doc format
		resp = tester.get('/literature/1/fake').data
		assert "Redirecting..." in resp
		resp = tester.get('/literature/1/fake/').data
		assert "Redirecting..." in resp
		#Test fake doc real format
		resp = tester.get('/literature/1000/html').data
		assert "Redirecting..." in resp
		resp = tester.get('/literature/1000/html/').data
		assert "Redirecting..." in resp
		resp = tester.get('/literature/1000/pdf').data
		assert "Redirecting..." in resp
		resp = tester.get('/literature/1000/pdf/').data
		assert "Redirecting..." in resp
		#Test fake doc fake format
		resp = tester.get('/literature/1000/fake').data
		assert "Redirecting..." in resp
		resp = tester.get('/literature/1000/fake/').data
		assert "Redirecting..." in resp

	#Test old link rerouting
	def test_retroute(self):
		tester = app.test_client(self)
		#Test real html redirect
		resp = tester.get('/bitcoin.html').data
		assert "Redirecting..." in resp
		#Test real other form redirect
		resp = tester.get('/bitcoin.pdf').data
		assert "Redirecting..." in resp
		#Test real slug fake format
		resp = tester.get('/bitcoin.fake').data
		assert "Redirecting..." in resp
		#Test fake html
		resp = tester.get('/fake-slug.html').data
		assert "Redirecting..." in resp
		#Test fake other format
		resp = tester.get('/fake-slug.pdf').data
		assert "Redirecting..." in resp
		#Test fake and fake format
		resp = tester.get('/fake-slug.fake').data
		assert "Redirecting..." in resp

if __name__ == '__main__':
	unittest.main()