import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SERVER_NAME = os.environ.get("SERVER_NAME", "sni:5000")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLATPAGES_ROOT = "pages"
    FLATPAGES_EXTENSION_CONFIGS = {
        "extra": {},
    }
    FLATPAGES_MARKDOWN_EXTENSIONS = ["extra"]
    FLATPAGES_EXTENSION = [".html", ".md"]
    CACHE_NO_NULL_WARNING = os.environ.get("CACHE_NO_NULL_WARNING", True)

    CSRF_ENABLED = True
