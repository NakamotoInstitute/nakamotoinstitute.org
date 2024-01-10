from enum import Enum, unique
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str | None = (
        "postgresql+psycopg://myuser:mysecretpassword@127.0.0.1:5432/mydatabase"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool | None = False
    ENVIRONMENT: Literal["development", "production"] = "production"
    CDN_ACCESS_KEY: str | None = None
    CDN_SECRET_KEY: str | None = None
    CDN_BUCKET_NAME: str | None = None
    CDN_ENDPOINT_URL: str | None = None
    CDN_BASE_URL: str | None = None

    @model_validator(mode="after")
    def check_cdn_settings(self) -> "Settings":
        if self.ENVIRONMENT == "production":
            variables = {
                "CDN_ACCESS_KEY": self.CDN_ACCESS_KEY,
                "CDN_SECRET_KEY": self.CDN_SECRET_KEY,
                "CDN_BUCKET_NAME": self.CDN_BUCKET_NAME,
                "CDN_ENDPOINT_URL": self.CDN_ENDPOINT_URL,
                "CDN_BASE_URL": self.CDN_BASE_URL,
            }

            for var_name, var_value in variables.items():
                if var_value is None:
                    raise ValueError(
                        f"{var_name} must not be None when ENVIRONMENT is 'production'"
                    )
        elif self.CDN_BASE_URL is None:
            self.CDN_BASE_URL = "http://localhost:8000/static"

        return self


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
