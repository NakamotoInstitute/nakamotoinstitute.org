import datetime
import re
from typing import List, Optional

from pydantic import AliasPath, BaseModel, Field, field_serializer, field_validator
from pydantic.alias_generators import to_camel

from ..authors.schemas import AuthorSchema


class LibraryCanonicalMDSchema(BaseModel):
    authors: List[str]
    date: str | int | datetime.date
    granularity: str = None
    image: Optional[str] = None
    doctype: str

    @field_validator("date")
    def parse_date(cls, value: str | int | datetime.date) -> datetime.date:
        if isinstance(value, str):
            if re.match(r"^\d{4}-\d{2}$", value):  # E.g. 2022-09
                parsed_date = datetime.datetime.strptime(f"{value}-01", "%Y-%m-%d")
                cls.granularity = "MONTH"
            elif re.match(r"^\d{4}$", value):  # E.g. 2022
                parsed_date = datetime.datetime.strptime(f"{value}-01-01", "%Y-%m-%d")
                cls.granularity = "YEAR"
            else:
                raise ValueError("Invalid string date format")

        elif isinstance(value, int):
            parsed_date = datetime.date(value, 1, 1)
            cls.granularity = "YEAR"

        elif isinstance(value, datetime.date):
            parsed_date = datetime.date(value.year, value.month, value.day)
            cls.granularity = "DAY"

        else:
            raise ValueError("Invalid date format")

        return parsed_date

    @field_validator("granularity")
    def set_granularity(cls, v, values):
        return cls.granularity or v


class LibraryMDSchema(BaseModel):
    title: str
    subtitle: Optional[str] = None
    display_title: Optional[str] = None
    sort_title: Optional[str] = None
    image_alt: Optional[str] = None
    formats: Optional[List[str]] = []


class LibraryTranslatedMDSchema(LibraryMDSchema):
    slug: Optional[str] = None


class DocumentTranslationSchema(BaseModel):
    language: str
    title: str
    slug: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class DocumentFormatSchema(BaseModel):
    format_type: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class LibraryDocBaseSchema(BaseModel):
    language: str
    title: str
    slug: str
    date: datetime.date = Field(alias=AliasPath("document", "date"))
    granularity: str = Field(alias=AliasPath("document", "granularity"))
    authors: List[AuthorSchema] = Field(alias=AliasPath("document", "authors"))
    translations: List[DocumentTranslationSchema]
    formats: List[DocumentFormatSchema]

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True

    @field_serializer("date")
    def serialize_date(self, date: datetime.date) -> str:
        return date.isoformat()

    @field_serializer("formats")
    def serialize_formats(self, formats) -> List[str]:
        """Convert DocumentFormatSchema to format_type string."""
        return sorted([fmt.format_type for fmt in formats])


class LibraryDocSchema(LibraryDocBaseSchema):
    content: str
