from sni.content.markdown import (
    ManifestBasedTranslatedHandler,
    TranslatedHandler,
    create_directory_translated_importer,
    create_translated_importer,
)
from sni.content.yaml import import_yaml_weights
from sni.database import SessionLocalSync
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


class LibraryHandler(TranslatedHandler):
    def process_canonical_data(self, canonical_data, fs_record):
        canonical_data["authors"] = [
            get(Author, db_session=self.session, slug=author)
            for author in canonical_data.pop("authors", [])
        ]
        return canonical_data

    def process_translation_data(
        self, translation_data, locale, canonical_translation, fs_record
    ):
        translation_data["formats"] = load_formats(
            self.session, translation_data.pop("formats", [])
        )
        translation_data["translators"] = [
            get(Translator, db_session=self.session, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        if locale != "en":
            translation_data["external"] = (
                translation_data.get("external") or canonical_translation.external
            )
        return translation_data


def import_library(directory: str, force: bool = False):
    with SessionLocalSync() as session:
        importer = create_translated_importer(
            directory=directory,
            session=session,
            handler_class=LibraryHandler,
            canonical_model=Document,
            translation_model=DocumentTranslation,
            schemas={
                "canonical": DocumentCanonicalMDModel,
                "translation": DocumentTranslationMDModel,
            },
            content_key="document",
            force=force,
        )
        importer.run()


class LibraryBookHandler(ManifestBasedTranslatedHandler):
    def process_canonical_data(self, canonical_data, fs_record):
        canonical_data["authors"] = [
            get(Author, db_session=self.session, slug=author)
            for author in canonical_data.pop("authors", [])
        ]
        return canonical_data

    def process_translation_data(
        self, translation_data, locale, canonical_translation, fs_record
    ):
        translation_data["formats"] = load_formats(
            self.session, translation_data.pop("formats", [])
        )
        translation_data["translators"] = [
            get(Translator, db_session=self.session, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        if locale != "en":
            translation_data["external"] = (
                translation_data.get("external") or canonical_translation.external
            )
        return translation_data


def import_library_books(directory: str, force: bool = False):
    with SessionLocalSync() as session:
        importer = create_directory_translated_importer(
            directory=directory,
            session=session,
            handler_class=LibraryBookHandler,  # custom logic for library books
            canonical_model=Document,
            translation_model=DocumentTranslation,
            node_model=DocumentNode,
            schemas={
                "manifest": BookMDModel,
                "canonical": DocumentCanonicalMDModel,
                "translation": DocumentTranslationMDModel,
                "node_content": BookMDNodeModel,
            },
            content_key="document",
            content_reference_id="document_translation_id",
            force=force,
        )
        importer.run()
