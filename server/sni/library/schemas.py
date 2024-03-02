import datetime
import re
from typing import Any, Literal

from pydantic import AliasPath, BaseModel, Field, field_serializer, model_validator

from sni.constants import DocumentFormats, Locales

from ..authors.schemas.base import AuthorModel
from ..shared.schemas import ORMModel, TranslationSchema
from ..translators.schemas import TranslatorModel

Granularity = Literal["DAY", "MONTH", "YEAR"]


class DocumentCanonicalMDModel(BaseModel):
    authors: list[str]
    date: str | int | datetime.date
    granularity: Granularity
    image: str | None = None
    doctype: str
    has_math: bool = False

    @model_validator(mode="before")
    @classmethod
    def parse_date(cls, data: Any) -> Any:
        if isinstance(data, dict):
            date = data["date"]
            if isinstance(date, str):
                if re.match(r"^\d{4}-\d{2}$", date):  # E.g. 2022-09
                    data["date"] = datetime.datetime.strptime(
                        f"{date}-01", "%Y-%m-%d"
                    ).date()
                    data["granularity"] = "MONTH"
                elif re.match(r"^\d{4}$", date):  # E.g. 2022
                    data["date"] = datetime.datetime.strptime(
                        f"{date}-01-01", "%Y-%m-%d"
                    ).date()
                    data["granularity"] = "YEAR"
                else:
                    raise ValueError("Invalid string date format")

            elif isinstance(date, int):
                data["date"] = datetime.date(date, 1, 1)
                data["granularity"] = "YEAR"

            else:
                data["granularity"] = "DAY"

        return data


class DocumentMDModel(BaseModel):
    title: str
    subtitle: str | None = None
    display_title: str | None = None
    external: str | None = None
    sort_title: str | None = None
    image_alt: str | None = None
    formats: list[DocumentFormats] = []

    @model_validator(mode="after")
    def check_sort_title(self) -> "DocumentMDModel":
        self.sort_title = self.sort_title or self.title
        return self


class DocumentTranslationMDModel(DocumentMDModel):
    slug: str | None = None
    external: str | None = None
    translators: list[str] = []


class DocumentFormatModel(ORMModel):
    url: str
    type: DocumentFormats


class DocumentBaseModel(ORMModel):
    locale: Locales
    title: str
    slug: str
    date: datetime.date = Field(validation_alias=AliasPath("document", "date"))
    granularity: str = Field(validation_alias=AliasPath("document", "granularity"))
    external: str | None
    authors: list[AuthorModel] = Field(
        validation_alias=AliasPath("document", "authors")
    )
    translations: list[TranslationSchema]
    formats: list[DocumentFormatModel] = Field(validation_alias="serialized_formats")

    @field_serializer("date")
    def serialize_date(self, date: datetime.date) -> str:
        return date.isoformat()


class DocumentIndexModel(DocumentBaseModel):
    has_content: bool = False

    @model_validator(mode="before")
    @classmethod
    def check_content(cls, data: Any) -> Any:
        data.has_content = bool(data.html_content)
        return data


class DocumentModel(DocumentBaseModel):
    html_content: str = Field(alias="content")
    subtitle: str | None
    display_title: str | None
    image: str | None = Field(validation_alias=AliasPath("document", "image_url"))
    image_alt: str | None
    has_math: bool = Field(
        validation_alias=AliasPath("document", "has_math"),
        serialization_alias="hasMath",
    )
    translators: list[TranslatorModel]
