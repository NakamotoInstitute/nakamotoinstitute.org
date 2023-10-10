import datetime
import re
from typing import Any, List, Optional

from pydantic import AliasPath, BaseModel, Field, field_serializer, model_validator
from pydantic.alias_generators import to_camel

from ..authors.schemas import AuthorModel
from ..shared.schemas import TranslationSchema
from ..translators.schemas import TranslatorModel


class DocumentCanonicalMDModel(BaseModel):
    authors: List[str]
    date: str | int | datetime.date
    granularity: str = None
    image: Optional[str] = None
    doctype: str

    @model_validator(mode="after")
    @classmethod
    def parse_date(cls, data: Any) -> Any:
        date = data.date
        if isinstance(date, str):
            if re.match(r"^\d{4}-\d{2}$", date):  # E.g. 2022-09
                data.date = datetime.datetime.strptime(f"{date}-01", "%Y-%m-%d").date()
                data.granularity = "MONTH"
            elif re.match(r"^\d{4}$", date):  # E.g. 2022
                data.date = datetime.datetime.strptime(
                    f"{date}-01-01", "%Y-%m-%d"
                ).date()
                data.granularity = "YEAR"
            else:
                raise ValueError("Invalid string date format")

        elif isinstance(date, int):
            data.date = datetime.date(date, 1, 1)
            data.granularity = "YEAR"

        else:
            data.granularity = "DAY"

        return data


class DocumentMDModel(BaseModel):
    title: str
    subtitle: Optional[str] = None
    display_title: Optional[str] = None
    sort_title: Optional[str] = None
    image_alt: Optional[str] = None
    formats: Optional[List[str]] = []

    @model_validator(mode="after")
    def check_sort_title(self) -> "DocumentMDModel":
        self.sort_title = self.sort_title or self.title
        return self


class DocumentTranslationMDModel(DocumentMDModel):
    slug: Optional[str] = None
    translators: Optional[List[str]] = []


class DocumentFormatModel(BaseModel):
    format_type: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class DocumentBaseModel(BaseModel):
    locale: str
    title: str
    slug: str
    date: datetime.date = Field(alias=AliasPath("document", "date"))
    granularity: str = Field(alias=AliasPath("document", "granularity"))
    external: Optional[str] = Field(alias=AliasPath("document", "external"))
    authors: List[AuthorModel] = Field(alias=AliasPath("document", "authors"))
    translations: List[TranslationSchema]
    translators: List[TranslatorModel]
    formats: List[DocumentFormatModel]

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True

    @field_serializer("date")
    def serialize_date(self, date: datetime.date) -> str:
        return date.isoformat()

    @field_serializer("formats")
    def serialize_formats(self, formats) -> List[str]:
        """Convert DocumentFormatModel to format_type string."""
        return sorted([fmt.format_type for fmt in formats])


class DocumentIndexModel(DocumentBaseModel):
    has_content: bool = False

    @model_validator(mode="before")
    @classmethod
    def check_content(cls, data: Any) -> Any:
        data.has_content = bool(data.content)
        return data


class DocumentModel(DocumentBaseModel):
    content: str
    subtitle: Optional[str] = None
    display_title: Optional[str] = None
    image: Optional[str] = Field(alias=AliasPath("document", "image"))
    image_alt: Optional[str] = None
