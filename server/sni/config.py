from enum import Enum, unique
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str | None = (
        "postgresql+psycopg://myuser:mysecretpassword@127.0.0.1:5432/mydatabase"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool | None = False
    ENVIRONMENT: Literal["development", "production"] = "production"


settings = Settings()


@unique
class Locales(str, Enum):
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


LocaleType = Literal[
    Locales.ARABIC.value,
    Locales.GERMAN.value,
    Locales.ENGLISH.value,
    Locales.SPANISH.value,
    Locales.PERSIAN.value,
    Locales.FINNISH.value,
    Locales.FRENCH.value,
    Locales.HEBREW.value,
    Locales.ITALIAN.value,
    Locales.PORTUGUESE.value,
    Locales.RUSSIAN.value,
    Locales.CHINESE.value,
]


@unique
class DocumentFormats(Enum):
    PDF = "pdf"
    EPUB = "epub"
    MOBI = "mobi"
    TXT = "txt"
