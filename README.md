Satoshi Nakamoto Institute
===========

NakamotoInstitute.org was written in Flask. 


## Guide to Installing SNI Locally

1. Install [PostgreSQL](http://www.postgresql.org/)

2. Create a user and a new database ([Instructions](http://killtheyak.com/use-postgresql-with-django-flask/)).

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

5. Update config.py if you would like to change "sni" in step 4 to a different [domain]:

6. Change the links in satoshiposts.json to http://sni:5000 (or the SERVER_NAME of your choice).

7. Download the PDFs and txts [here](http://nakamotoinstitute.org/static/docs/sni-docs.zip) and place them in /static/templates/docs

8. Set up a virtualenv with <code>virtualenv --no-site-packages venv </code> and <code>. venv/bin/activate </code>

9. Install the dependencies using <code>pip install -r requirements.txt</code>.

10. In a Python console run <code> from sni import db </code> and <code> db.create_all() </code>

11. Run <code>python dataimport.py</code>. The db will be cleared and re-populated each time you do this.

12. Run <code>python run.py runserver</code> and navigate to sni:5000 in your browser.

13. Migrations are done with [Flask-Migrate](http://flask-migrate.readthedocs.org/en/latest/). You can start enable migrations by running:<br /> <code>python run.py db init</code>




## How You Can Help

* Format the HTML literature templates
* Adjust the CSS and HTML to improve readability and navigation
* Write tests for the Python code

--

NakamotoInstitute.org is under the GNU Affero License.
