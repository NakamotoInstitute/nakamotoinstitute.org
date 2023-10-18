import os

import click

from sni.cli.utils import (
    DONE,
    extract_data_from_filename,
    process_canonical_file,
    process_translated_file,
)
from sni.extensions import db
from sni.mempool.schemas import (
    MempoolSeriesCanonicalMDModel,
    MempoolSeriesMDModel,
    MempoolSeriesTranslationMDModel,
)
from sni.models import BlogSeries, BlogSeriesTranslation


def process_and_add_canonical_series_file(
    filepath: str, slug: str, blog_series: dict, canonical_schema, schema
):
    (
        validated_canonical_data,
        validated_translation_data,
        content,
    ) = process_canonical_file(filepath, canonical_schema, schema)

    canonical_data = validated_canonical_data.dict()
    translation_data = validated_translation_data.dict()

    new_blog_series = BlogSeries(**canonical_data)
    db.session.add(new_blog_series)
    db.session.flush()

    blog_series_translation = BlogSeriesTranslation(
        **translation_data,
        slug=slug,
        locale="en",
        content=content,
        blog_series=new_blog_series,
    )
    db.session.add(blog_series_translation)

    blog_series[slug] = {
        "canonical": new_blog_series,
        "translation": blog_series_translation,
    }


def process_and_add_translated_series_file(
    filepath: str, slug: str, locale: str, blog_series: dict, translated_schema
):
    validated_translation_data, content = process_translated_file(
        filepath, translated_schema
    )

    translation_data = validated_translation_data.dict()
    series = blog_series.get(slug)

    if not series:
        return

    translation_data["slug"] = translation_data.get("slug") or slug
    blog_series_translation = BlogSeriesTranslation(
        **translation_data,
        locale=locale,
        content=content,
        blog_series=blog_series["canonical"],
    )
    db.session.add(blog_series_translation)


def import_series_content(
    directory_path: str, canonical_schema, schema, translated_schema
):
    blog_series = {}
    english_filenames = []
    non_english_filenames = []

    for filename in sorted(os.listdir(directory_path)):
        _, locale, _ = extract_data_from_filename(filename)
        if locale == "en":
            english_filenames.append(filename)
        else:
            non_english_filenames.append(filename)

    for filename in english_filenames:
        filepath = os.path.join(directory_path, filename)
        slug, _, _ = extract_data_from_filename(filename)
        process_and_add_canonical_series_file(
            filepath, slug, blog_series, canonical_schema, schema
        )

    for filename in non_english_filenames:
        filepath = os.path.join(directory_path, filename)
        slug, locale, _ = extract_data_from_filename(filename)
        process_and_add_translated_series_file(
            filepath, slug, locale, blog_series, translated_schema
        )

    db.session.commit()


def import_mempool_series():
    click.echo("Importing Mempool series...", nl=False)
    import_series_content(
        "content/mempool_series",
        MempoolSeriesCanonicalMDModel,
        MempoolSeriesMDModel,
        MempoolSeriesTranslationMDModel,
    )
    click.echo(DONE)
