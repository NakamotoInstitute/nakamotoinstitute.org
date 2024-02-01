from pydantic import model_validator
from pydantic_settings import BaseSettings

from .constants import Environment

DEFAULT_BASE_URL = "http://localhost:8000"
DEBUG_CDN_BASE_URL = f"{DEFAULT_BASE_URL}/static"


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str | None = (
        "postgresql+psycopg://myuser:mysecretpassword@127.0.0.1:5432/mydatabase"
    )
    ENVIRONMENT: Environment = Environment.PRODUCTION
    BASE_URL: str | None = None
    CDN_ACCESS_KEY: str | None = None
    CDN_SECRET_KEY: str | None = None
    CDN_BUCKET_NAME: str | None = None
    CDN_ENDPOINT_URL: str | None = None
    CDN_BASE_URL: str | None = None

    @model_validator(mode="after")
    def check_base_url(self) -> "Settings":
        if self.ENVIRONMENT.is_debug and self.BASE_URL is None:
            self.BASE_URL = DEFAULT_BASE_URL
        return self

    @model_validator(mode="after")
    def check_cdn_settings(self) -> "Settings":
        if self.ENVIRONMENT.is_deployed:
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
            self.CDN_BASE_URL = DEBUG_CDN_BASE_URL

        return self


settings = Settings()
