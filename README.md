Satoshi Nakamoto Institute
===========

NakamotoInstitute.org was written in Flask. 


## Guide to Installing SNI Locally

1. Install [PostgreSQL](http://www.postgresql.org/)

2. Create a user and a new database ([Debian instructions](https://wiki.debian.org/PostgreSql)).

3. Apply your settings from step 2 in config.py:


<code>SQLALCHEMY_DATABASE_URI = "postgresql://[user]:[password]@localhost/[db name]?client_encoding=utf8"</code>


3. Update your /etc/hosts file:

<<<<<<< HEAD
    127.0.0.1     localhost

    127.0.0.1     sni
    
    127.0.0.1     satoshi.sni


3. Update config.py if you would like to change "sni" to a different domain.
=======
    127.0.0.1     localhost <br />
    127.0.0.1     sni <br />
    127.0.0.1     satoshi.sni <br />

3. Update config.py if you would like to change "sni" in step 3 to a different [domain]:

<code> SERVER_NAME = '[domain]:5000' </code>
>>>>>>> 0a5b846ffe900909c0bdd2d5a68685357e57db82

4. Change the links in satoshiposts.json to http://sni:5000 (or the SERVER_NAME of your choice).

5. Download the PDFs and txts [here](http://nakamotoinstitute.org/static/docs/sni-docs.zip) and place them in /static/templates/docs

6. Set up a virtualenv 

8. Install the dependencies using <code>pip install -r requirements.txt</code>.

9. In a Python console run <code> from sni import db </code> and <code> db.create_all() </code>

10. Run <code>python dataimport.py</code>. The db will be cleared and re-populated each time you do this.

11. Run <code>python run.py runserver</code> and navigate to sni:5000 in your browser.

12. Migrations are done with [Flask-Migrate](http://flask-migrate.readthedocs.org/en/latest/).




## How You Can Help

* Format the HTML literature templates
* Adjust the CSS and HTML to improve readability and navigation
* Improve tests.py

--

NakamotoInstitute.org is under the GNU Affero License.
