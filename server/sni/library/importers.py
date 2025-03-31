from sni.content.markdown import MarkdownDirectoryImporter, TranslatedMarkdownImporter
from sni.content.yaml import import_yaml_weights
from sni.models import (
    Author,
    Document,
    DocumentFormat,
    DocumentNode,
    DocumentTranslation,
    Translator,
)
from sni.shared.service import get, get_or_create

from .schemas import (
    BookMDModel,
    BookMDNodeModel,
    DocumentCanonicalMDModel,
    DocumentTranslationMDModel,
    Node,
)


def import_library_weights(
    db_session, force: bool = False, force_conditions: list[bool] = []
):
    return import_yaml_weights(
        db_session,
        Document,
        "data/weights/library.yaml",
        force=force or any(force_conditions),
    )


def load_formats(db_session, formats):
    loaded_formats = []
    for fmt in formats:
        if isinstance(fmt, str):
            fmt = {"type": fmt}
        loaded_formats.append(
            get_or_create(
                DocumentFormat,
                db_session=db_session,
                format_type=fmt["type"],
                volume=fmt.get("volume"),
            )
        )
    return loaded_formats


class LibraryImporter(TranslatedMarkdownImporter):
    directory_path = "content/library"
    content_type = "Library"
    canonical_model = Document
    translation_model = DocumentTranslation
    canonical_schema = DocumentCanonicalMDModel
    translation_schema = DocumentTranslationMDModel
    content_key = "document"

    def process_canonical_additional_data(self, canonical_data):
        canonical_data["authors"] = [
            get(Author, db_session=self.db_session, slug=author)
            for author in canonical_data.pop("authors", [])
        ]
        return canonical_data

    def process_translation_additional_data(
        self, translation_data, canonical_entry, metadata
    ):
        translation_data["formats"] = load_formats(
            self.db_session, translation_data.pop("formats", [])
        )
        translation_data["translators"] = [
            get(Translator, db_session=self.db_session, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        return super().process_translation_additional_data(
            translation_data, canonical_entry, metadata
        )

    def process_translation_for_translated_file(
        self, translation_data, canonical_entry, metadata
    ):
        translation_data["external"] = (
            translation_data.get("external") or canonical_entry["translation"].external
        )
        translation_data["formats"] = load_formats(
            self.db_session, translation_data.pop("formats", [])
        )
        translation_data["translators"] = [
            get(Translator, db_session=self.db_session, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]

        return super().process_translation_for_translated_file(
            translation_data, canonical_entry, metadata
        )


class LibraryBookImporter(MarkdownDirectoryImporter):
    directory_path = "content/library"
    content_type = "Library Books"
    canonical_model = Document
    translation_model = DocumentTranslation
    node_model = DocumentNode
    canonical_schema = DocumentCanonicalMDModel
    translation_schema = DocumentTranslationMDModel
    manifest_schema = BookMDModel
    node_schema = Node
    node_content_schema = BookMDNodeModel
    content_reference_id = "document_translation_id"
    content_key = "document"

    def process_canonical_additional_data(self, canonical_data):
        canonical_data["authors"] = [
            get(Author, db_session=self.db_session, slug=author)
            for author in canonical_data.pop("authors", [])
        ]
        return canonical_data

    def process_translation_additional_data(
        self, translation_data, canonical_entry, metadata
    ):
        translation_data["formats"] = load_formats(
            self.db_session, translation_data.pop("formats", [])
        )
        translation_data["translators"] = [
            get(Translator, db_session=self.db_session, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        return super().process_translation_additional_data(
            translation_data, canonical_entry, metadata
        )
