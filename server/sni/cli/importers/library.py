from sni.authors.models import Author
from sni.cli.utils import (
    ContentImporter,
    get,
    get_or_create,
    process_translated_file,
)
from sni.extensions import db
from sni.library.models import Document, DocumentFormat, DocumentTranslation
from sni.library.schemas import (
    DocumentCanonicalMDModel,
    DocumentMDModel,
    DocumentTranslationMDModel,
)
from sni.translators.models import Translator


class LibraryImporter(ContentImporter):
    content_type = "library"
    canonical_model = Document
    translation_model = DocumentTranslation
    canonical_schema = DocumentCanonicalMDModel
    md_schema = DocumentMDModel
    translation_schema = DocumentTranslationMDModel
    content_key = "document"

    def process_canonical_additional_data(self, canonical_data):
        canonical_data["authors"] = [
            get(Author, slug=author) for author in canonical_data.pop("authors", [])
        ]
        return canonical_data

    def process_translation_additional_data(
        self, translation_data, canonical_entry, slug, content
    ):
        translation_data["formats"] = [
            get_or_create(DocumentFormat, format_type=fmt)
            for fmt in translation_data.pop("formats", [])
        ]
        translation_data["translators"] = [
            get(Translator, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        return translation_data

    def process_and_add_translated_file(self, filepath, slug, locale):
        validated_translation_data, content = process_translated_file(
            filepath, self.translation_schema
        )

        translation_data = validated_translation_data.dict()
        document = self.content_map.get(slug)

        if not document:
            return

        translation_data["slug"] = translation_data.get("slug") or slug
        translation_data["formats"] = [
            get_or_create(DocumentFormat, format_type=fmt)
            for fmt in translation_data.pop("formats")
        ]
        translation_data["translators"] = [
            get(Translator, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        document_translation = self.translation_model(
            **translation_data,
            locale=locale,
            content=content,
            document=document["canonical"],
        )
        db.session.add(document_translation)


def import_library():
    library_importer = LibraryImporter(directory_path="content/library")
    library_importer.run_import()
