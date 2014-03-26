Satoshi Nakamoto Institute
===========

Our website was written in Flask. Set up a virtualenv and install the dependencies using <code>pip install -r requirements.txt</code>.

## Some Notes

To get subdomains to work on your machine, update your /etc/hosts file:

    127.0.0.1     localhost
    127.0.0.1     sni
    127.0.0.1     satoshi.sni

You can change sni to anything else. Just be sure to update config.py

--

The static docs folder does not contain the PDFs because of the large size. All of the files in this folder, including PDFs and txts can be obtained in a zip file at http://nakamotoinstitute.org/static/docs/sni-docs.zip

--

To import JSONs to db, run <code>python dataimport.py</code>. The db will be cleared and re-populated each time you do this.

--

The links in satoshiposts.json must be changed to http://sni:5000 (or the SERVER_NAME of your choice).

--

Migrations are done using [Flask-Migrate](http://flask-migrate.readthedocs.org/en/latest/).

## How You Can Help

Help us:

* Make the site look nicer. We are not graphic designers.
* Write actually functional tests.
* Format the HTML literature templates.

--

Our website is under the GNU Affero License.