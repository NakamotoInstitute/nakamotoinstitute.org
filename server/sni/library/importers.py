from sni.content.markdown import TranslatedMarkdownImporter
from sni.models import Author, Document, DocumentFormat, DocumentTranslation, Translator
from sni.shared.service import get, get_or_create

from .schemas import (
    DocumentCanonicalMDModel,
    DocumentMDModel,
    DocumentTranslationMDModel,
)


class LibraryImporter(TranslatedMarkdownImporter):
    directory_path = "content/library"
    content_type = "Library"
    canonical_model = Document
    translation_model = DocumentTranslation
    canonical_schema = DocumentCanonicalMDModel
    md_schema = DocumentMDModel
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
        translation_data["formats"] = [
            get_or_create(DocumentFormat, db_session=self.db_session, format_type=fmt)
            for fmt in translation_data.pop("formats", [])
        ]
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
        translation_data["formats"] = [
            get_or_create(DocumentFormat, db_session=self.db_session, format_type=fmt)
            for fmt in translation_data.pop("formats")
        ]
        translation_data["translators"] = [
            get(Translator, db_session=self.db_session, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]

        return super().process_translation_for_translated_file(
            translation_data, canonical_entry, metadata
        )
