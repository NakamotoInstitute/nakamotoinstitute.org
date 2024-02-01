from enum import Enum, unique
from typing import Any, Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str | None = (
        "postgresql+psycopg://myuser:mysecretpassword@127.0.0.1:5432/mydatabase"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool | None = False
    ENVIRONMENT: Literal["development", "production"] = "production"
    BASE_URL: str
    CDN_ACCESS_KEY: str | None = None
    CDN_SECRET_KEY: str | None = None
    CDN_BUCKET_NAME: str | None = None
    CDN_ENDPOINT_URL: str | None = None
    CDN_BASE_URL: str | None = None

    @model_validator(mode="before")
    @classmethod
    def check_base_url(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "BASE_URL" not in data:
                if data.get("ENVIRONMENT") == "development":
                    data["BASE_URL"] = "http://localhost:8000"
        return data

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
    KOREAN = "ko"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    CHINESE_SIMPLIFIED = "zh-cn"


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
    Locales.KOREAN.value,
    Locales.PORTUGUESE.value,
    Locales.RUSSIAN.value,
    Locales.CHINESE_SIMPLIFIED.value,
]


@unique
class DocumentFormats(Enum):
    PDF = "pdf"
    EPUB = "epub"
    MOBI = "mobi"
    TXT = "txt"
