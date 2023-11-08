import os
from enum import Enum, unique

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_NO_NULL_WARNING = os.environ.get("CACHE_NO_NULL_WARNING", True)

    CSRF_ENABLED = True


@unique
class Locales(Enum):
    ARABIC = "ar"
    GERMAN = "de"
    ENGLISH = "en"
    SPANISH = "es"
    PERSIAN = "fa"
    FINNISH = "fi"
    FRENCH = "fr"
    HEBREW = "he"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    CHINESE = "zh"


@unique
class DocumentFormats(Enum):
    PDF = "pdf"
    EPUB = "epub"
    MOBI = "mobi"
    TXT = "txt"
