Satoshi Nakamoto Institute
===========

NakamotoInstitute.org was written in Flask.


## Guide to Installing SNI Locally

1. Install [SQLite](https://www.sqlite.org/index.html), [python3](https://www.python.org/), and [virtualenv](https://virtualenv.pypa.io/en/latest/)

2. Update your /etc/hosts file:
  ```
  127.0.0.1     localhost
  127.0.0.1     sni
  127.0.0.1     satoshi.sni
  ```

3. Update the domain assigned to `SERVER_NAME` in `config.py` if you would like to change "sni"

5. Download the PDFs and txts [here](https://nakamotoinstitute.org/static/docs/sni-docs.zip) and place them in `/static/templates/docs`

6. Set up a virtualenv with `virtualenv -p python3 --no-site-packages venv` and `. venv/bin/activate`

7. Install the dependencies using `pip install -r requirements.txt`.

8. Run `mkdir tmp`

9. Run `./dataimport.py`. The db will be cleared and re-populated each time you do this.

10. Run `./run.py runserver` and navigate to `sni:5000` in your browser.

## How You Can Help

* Format the HTML literature templates
* Adjust the CSS and HTML to improve readability and navigation
* Write tests for the Python code

***

NakamotoInstitute.org is under the GNU Affero License.
