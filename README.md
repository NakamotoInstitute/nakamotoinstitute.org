Satoshi Nakamoto Institute
===========

NakamotoInstitute.org was written in Flask.


## Guide to Installing SNI Locally

1. Install [python3](https://www.python.org/) and [virtualenv](https://virtualenv.pypa.io/en/latest/)

2. Copy `config.py.env` to `config.py`

3. Update the domain assigned to `SERVER_NAME` in `config.py` if you would like to change "sni"

4. If you are running the app locally, change `FLASK_DEBUG` in `config.py` to `True` in order to enable reloading of the server on code changes.

5. Update your /etc/hosts file (replace `sni` with the value from step 3 if you changed it):
  ```
  127.0.0.1     localhost
  127.0.0.1     sni
  127.0.0.1     satoshi.sni
  ```

6. Download the PDFs and txts [here](https://nakamotoinstitute.org/static/docs/sni-docs.zip) and place them in `sni/static/docs`

7. Set up a virtualenv with `virtualenv -p python3 --no-site-packages venv` and `. venv/bin/activate`

8. Install the dependencies using `pip install -r requirements.txt`.

9. Run `mkdir tmp`

10. Run `./dataimport.py update`. The db will be cleared and re-populated each time you do this. You can use the flags `--content`, and `--skeptic` to repopulate only models associated with the blog, the docs, and research docs, or skeptics, respectively.

11. Run `./run.py runserver` and navigate to `sni:5000` in your browser.

## How You Can Help

* Format the HTML literature templates
* Adjust the CSS and HTML to improve readability and navigation
* Write tests for the Python code

***

NakamotoInstitute.org is under the GNU Affero License.
