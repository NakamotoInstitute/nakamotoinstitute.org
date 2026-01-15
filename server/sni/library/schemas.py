import datetime
import os
import re
from typing import Any, Literal, Union

from pydantic import AliasPath, BaseModel, Field, field_serializer, model_validator

from sni.constants import DocumentFormats, Locales
from sni.shared.schemas import SlugParamModel

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
    purchase_link: str | None = None

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


class DocumentFormat(BaseModel):
    type: DocumentFormats
    volume: int | None = None


class DocumentMDModel(BaseModel):
    title: str
    subtitle: str | None = None
    external: str | None = None
    sort_title: str | None = None
    image_alt: str | None = None
    formats: list[DocumentFormat] = []

    @model_validator(mode="after")
    def check_sort_title(self) -> "DocumentMDModel":
        self.sort_title = self.sort_title or self.title
        return self

    @model_validator(mode="before")
    @classmethod
    def parse_formats(cls, data: Any) -> Any:
        if isinstance(data, dict) and "formats" in data:
            formats = []
            for fmt in data["formats"]:
                if isinstance(fmt, str):
                    formats.append({"type": fmt})  # Convert "pdf" -> {"type": "pdf"}
                else:
                    formats.append(fmt)  # Keep {"type": "pdf", "volume": 1} as is
            data["formats"] = formats
        return data


class DocumentTranslationMDModel(DocumentMDModel):
    slug: str | None = None
    display_title: str | None = None
    display_date: str | None = None
    external: str | None = None
    translators: list[str] = []


NodeType = Union[str, "Node"]
NodeListType = list[NodeType]


class Node(BaseModel):
    slug: str
    children: NodeListType = []

    @classmethod
    def parse_node(cls, node):
        if isinstance(node, str):
            return node
        elif isinstance(node, dict):
            for key, value in node.items():
                return cls(
                    slug=key, children=[cls.parse_node(child) for child in value]
                )
        else:
            raise ValueError(f"Invalid node type: {type(node)}")


class BookMDModel(BaseModel):
    nodes: NodeListType

    @classmethod
    def parse_nodes(cls, nodes):
        return [Node.parse_node(node) for node in nodes]

    @model_validator(mode="before")
    @classmethod
    def parse_front_matter(cls, data: Any) -> Any:
        if isinstance(data, dict):
            data["nodes"] = cls.parse_nodes(data.get("nodes", []))
        return data

    def gather_markdown_files(self, base_path) -> list[tuple[str, str | None, int]]:
        markdown_files = []

        def _gather_files(node, parent, current_path, order):
            if isinstance(node, str):
                markdown_files.append(
                    (os.path.join(current_path, f"{node}.md"), parent, order)
                )
            elif isinstance(node, Node):
                for idx, child in enumerate(node.children, start=1):
                    _gather_files(child, node.name, current_path, idx)

        for idx, node in enumerate(self.nodes, start=1):
            _gather_files(node, None, base_path, idx)

        return markdown_files


class BookMDNodeModel(BaseModel):
    heading: str | None = None
    title: str
    subheading: str | None = None
    nav_title: str | None = None


class DocumentFormatModel(ORMModel):
    url: str
    type: DocumentFormats
    volume: int | None = None


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
    flattened_nodes: list["DocumentNodeBaseModel"] = Field(serialization_alias="nodes")

    @model_validator(mode="before")
    @classmethod
    def check_content(cls, data: Any) -> Any:
        data.has_content = bool(data.content.html_content)
        return data


class DocumentNodeBaseModel(ORMModel):
    slug: str
    title: str
    nav_title: str | None = None


class DocumentModel(DocumentBaseModel):
    html_content: str = Field(
        validation_alias=AliasPath("content", "html_content"), alias="content"
    )
    subtitle: str | None
    display_title: str | None
    display_date: str | None
    image: str | None = Field(validation_alias=AliasPath("document", "image_url"))
    image_alt: str | None
    has_math: bool = Field(
        validation_alias=AliasPath("document", "has_math"),
        serialization_alias="hasMath",
    )
    translators: list[TranslatorModel]
    entry_node: DocumentNodeBaseModel | None
    purchase_link: str | None = Field(
        validation_alias=AliasPath("document", "purchase_link")
    )


class DocumentNodeModel(ORMModel):
    heading: str | None = None
    title: str
    subheading: str | None = None
    doc_title: str = Field(validation_alias=AliasPath("document_translation", "title"))
    doc_slug: str = Field(validation_alias=AliasPath("document_translation", "slug"))
    authors: list[AuthorModel] = Field(
        validation_alias=AliasPath("document_translation", "document", "authors")
    )
    translations: list[TranslationSchema] = Field(
        validation_alias=AliasPath("document_translation", "translations")
    )
    html_content: str = Field(alias="content")
    root_parent: DocumentNodeBaseModel | None = Field(alias="root")
    next_node: DocumentNodeBaseModel | None = Field(alias="next")
    previous_node: DocumentNodeBaseModel | None = Field(alias="previous")


class DocumentNodeParamsModel(SlugParamModel):
    node_slug: str
