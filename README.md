# Satoshi Nakamoto Institute

NakamotoInstitute.org was written in Python using Flask.

## Local Installation

1. Install [`python3`](https://www.python.org/) and [`virtualenv`](https://virtualenv.pypa.io/en/latest/)
1. Set up and activate a Python 3 virtualenv.
1. Install [`pip-tools`](https://github.com/jazzband/pip-tools)
1. Copy `.env.example` to `.env`.
1. Update the domain assigned to `SERVER_NAME` in `.env` if you would like something other than `sni`
1. Update your /etc/hosts file (replace `sni` with the value from step 3 if you changed it):
    ```
    127.0.0.1     localhost
    127.0.0.1     sni
    127.0.0.1     satoshi.sni
    ```
1. Download the PDFs and txts [here](https://nakamotoinstitute.org/static/docs/sni-docs.zip) and place them in `app/static/docs`
1. Install the dependencies using `pip-sync requirements/base.txt requirements/dev.txt`.
    - The requirements assume Python 3.9. If you are using a different version, you may need to regenerate the dependencies:
      ```
      $ pip-compile requirements/base.in
      $ pip-compile requirements/dev.in
      ```
1. Run `flask data seed`. The db will be cleared and re-populated each time you do this. The SQLite db can be found as `app.db`.
1. Run `flask run` and navigate to `sni:5000` in your browser.

## Adding Mempool Translations

1. Add proper markdown front matter:
    ```
    translated_title: # Name of title in local language
    translation_url: # Original URL for translation (optional)
    translation_publication: # Name of original publication hosting translation (optional)
    translation_publication_url: # URL of original publication hosting translation (optional)
    ```
1. Place the markdown file in `app/pages/mempool` with the filename `<slug>-<language ietf code>.md` (e.g. `speculative-attack-es.md`).
1. If you are a new translator, add your name and URL (i.e. website, Twitter, etc.) to `data/translators.json`.
1. Update `data/blogposts.json`:
    ```
    "translations": {
      "<local language code>": ["<translator name>"]
    }
    ```
    Note: the name must match that in `translators.json` exactly.

1. If you are submitting a new language, add it to `data/languages.json`.

## How You Can Help

* Adjust the CSS and HTML to improve readability and navigation
* Write tests for the Python code
* Submit translations of website content (literature translations coming soon!)

***

NakamotoInstitute.org is under the GNU Affero License.
