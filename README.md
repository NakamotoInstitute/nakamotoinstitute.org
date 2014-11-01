Satoshi Nakamoto Institute
===========

NakamotoInstitute.org was written in Flask.


## Guide to Installing SNI Locally

1. Install [PostgreSQL](http://www.postgresql.org/)

2. Create a user and a new database ([Instructions](http://killtheyak.com/use-postgresql-with-django-flask/))

3. Create file in the project's root folder called <code>config.py</code>:

````
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SERVER_NAME = 'sni:5000'
SQLALCHEMY_DATABASE_URI = "postgresql://[username]:[password]@sni/[database]"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DEBUG = False
CSRF_ENABLED = True
````

4. Update your /etc/hosts file:

    127.0.0.1     localhost <br />
    127.0.0.1     sni <br />
    127.0.0.1     satoshi.sni <br />

5. Update config.py if you would like to change "sni" in step 4 to a different [domain]


6. Download the PDFs and txts [here](http://nakamotoinstitute.org/static/docs/sni-docs.zip) and place them in /static/templates/docs

7. Set up a virtualenv with <code>virtualenv --no-site-packages venv</code> and <code>. venv/bin/activate </code>

8. Install the dependencies using <code>pip install -r requirements.txt</code>.

9. Run <code>createdb.py</code>

10. Run <code>python dataimport.py</code>. The db will be cleared and re-populated each time you do this.

11. [Generate new addresses](http://pacio.li/bitcoind/2014/10/31/how-to-connect-to-bitcoin-cores-json-rpc-api-with-python.html) and import them with <code>python importaddresses.py</code>

12. Run <code>python run.py runserver</code> and navigate to sni:5000 in your browser.


## Add a link to "the Skeptics" page

To add a link, fork the repo, add an entry to skeptics.json and make a pull request to 'the-skeptics' branch:

<code>git pull origin the-skeptics<code>

You can also email the information to contact@nakamotoinstitute.org


## How You Can Help

* Format the HTML literature templates
* Adjust the CSS and HTML to improve readability and navigation
* Write tests for the Python code

--

NakamotoInstitute.org is under the GNU Affero License.
