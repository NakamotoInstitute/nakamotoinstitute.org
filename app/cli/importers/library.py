import os

import click

from app import db
from app.cli.utils import (
    DONE,
    extract_data_from_filename,
    get,
    get_or_create,
    process_canonical_file,
    process_translated_file,
)
from app.library.schemas import (
    LibraryCanonicalMDSchema,
    LibraryMDSchema,
    LibraryTranslatedMDSchema,
)
from app.models import Author, Document, DocumentFormat, DocumentTranslation, Translator


def process_and_add_canonical_file(
    filepath: str, slug: str, documents: dict, canonical_schema, schema
):
    (
        validated_canonical_data,
        validated_translation_data,
        content,
    ) = process_canonical_file(filepath, canonical_schema, schema)

    canonical_data = validated_canonical_data.dict()
    translation_data = validated_translation_data.dict()

    authors = [get(Author, slug=author) for author in canonical_data.pop("authors")]

    document = Document(**canonical_data, authors=authors)
    db.session.add(document)
    db.session.flush()

    translation_data["formats"] = [
        get_or_create(DocumentFormat, format_type=fmt)
        for fmt in translation_data["formats"]
    ]
    translation_data["translators"] = [
        get(Translator, slug=slug) for slug in translation_data.pop("translators", [])
    ]
    document_translation = DocumentTranslation(
        **translation_data,
        slug=slug,
        language="en",
        content=content,
        document=document,
    )
    db.session.add(document_translation)

    documents[slug] = {"canonical": document, "translation": document_translation}


def process_and_add_translated_file(
    filepath: str, slug: str, lang: str, documents: dict, translated_schema
):
    validated_translation_data, content = process_translated_file(
        filepath, translated_schema
    )

    translation_data = validated_translation_data.dict()
    document = documents.get(slug)

    if not document:
        return

    translation_data["slug"] = translation_data.get("slug") or slug
    translation_data["formats"] = [
        get_or_create(DocumentFormat, format_type=fmt)
        for fmt in translation_data.pop("formats")
    ]
    translation_data["translators"] = [
        get(Translator, slug=slug) for slug in translation_data.pop("translators", [])
    ]
    document_translation = DocumentTranslation(
        **translation_data,
        language=lang,
        content=content,
        document=document["canonical"],
    )
    db.session.add(document_translation)


def import_content(directory_path: str, canonical_schema, schema, translated_schema):
    blog_posts = {}
    english_filenames = []
    non_english_filenames = []

    for filename in sorted(os.listdir(directory_path)):
        _, lang, _ = extract_data_from_filename(filename)
        if lang == "en":
            english_filenames.append(filename)
        else:
            non_english_filenames.append(filename)

    for filename in english_filenames:
        filepath = os.path.join(directory_path, filename)
        slug, _, _ = extract_data_from_filename(filename)
        process_and_add_canonical_file(
            filepath, slug, blog_posts, canonical_schema, schema
        )

    for filename in non_english_filenames:
        filepath = os.path.join(directory_path, filename)
        slug, lang, _ = extract_data_from_filename(filename)
        process_and_add_translated_file(
            filepath, slug, lang, blog_posts, translated_schema
        )

    db.session.commit()


def import_library():
    click.echo("Importing Library...", nl=False)
    import_content(
        "content/library",
        LibraryCanonicalMDSchema,
        LibraryMDSchema,
        LibraryTranslatedMDSchema,
    )
    click.echo(DONE)