from sni.authors.models import Author
from sni.cli.utils import (
    ContentImporter,
    get,
    get_or_create,
    process_canonical_file,
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

    def process_and_add_canonical_file(self, filepath, slug):
        (
            validated_canonical_data,
            validated_translation_data,
            content,
        ) = process_canonical_file(filepath, self.canonical_schema, self.md_schema)

        canonical_data = validated_canonical_data.dict()
        translation_data = validated_translation_data.dict()

        canonical_data["authors"] = [
            get(Author, slug=author) for author in canonical_data.pop("authors")
        ]

        document = self.canonical_model(**canonical_data)
        db.session.add(document)
        db.session.flush()

        translation_data["formats"] = [
            get_or_create(DocumentFormat, format_type=fmt)
            for fmt in translation_data["formats"]
        ]
        translation_data["translators"] = [
            get(Translator, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        document_translation = self.translation_model(
            **translation_data,
            slug=slug,
            locale="en",
            content=content,
            document=document,
        )
        db.session.add(document_translation)

        self.content_map[slug] = {
            "canonical": document,
            "translation": document_translation,
        }

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
