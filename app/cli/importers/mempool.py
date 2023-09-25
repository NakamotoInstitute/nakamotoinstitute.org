import os

import click

from app import db
from app.cli.utils import DONE, extract_data_from_filename, get, process_markdown_file
from app.models import Author, BlogPost, BlogPostTranslation
from app.schemas.data import MempoolMDSchema, MempoolTranslatedMDSchema


def _load_common_data(slug, lang, extension, directory_path, schema):
    filepath = os.path.join(directory_path, f"{slug}.{lang}.{extension}")
    front_matter_dict, remaining_content = process_markdown_file(filepath, schema)

    if front_matter_dict:
        return front_matter_dict, remaining_content
    return None, None


def process_english_file(filename, directory_path, blog_posts, blog_post_translations):
    slug, lang, extension = extract_data_from_filename(filename)
    front_matter_dict, remaining_content = _load_common_data(
        slug, lang, extension, directory_path, MempoolMDSchema
    )

    if not front_matter_dict:
        return

    keys_to_move = ["title", "excerpt", "image_alt"]
    translation_data = {"language": lang, "slug": slug, "content": remaining_content}
    for key in keys_to_move:
        translation_data[key] = front_matter_dict.pop(key, None)

    blog_posts[slug] = front_matter_dict
    blog_post_translations[slug] = [translation_data]


def process_other_language_file(filename, directory_path, blog_post_translations):
    slug, lang, extension = extract_data_from_filename(filename)
    front_matter_dict, remaining_content = _load_common_data(
        slug, lang, extension, directory_path, MempoolTranslatedMDSchema
    )

    if not front_matter_dict:
        return

    translation_data = {
        "language": lang,
        "slug": slug,
        "content": remaining_content,
        **front_matter_dict,
    }

    english_data = next(
        (item for item in blog_post_translations[slug] if item["language"] == "en"), {}
    )
    translation_data = {**english_data, **translation_data}

    blog_post_translations.setdefault(slug, []).append(translation_data)


def handle_translations_for_slug(slug, translations, blog_posts, db_session):
    blog_post_data = blog_posts.get(slug, {})

    if "author" in blog_post_data:
        blog_post_data["author"] = get(Author, slug=blog_post_data["author"])

    blog_post = BlogPost(**blog_post_data)
    db_session.add(blog_post)

    english_translation_data = next(
        (item for item in translations if item["language"] == "en"), None
    )

    if english_translation_data:
        blog_post_translation = BlogPostTranslation(
            **english_translation_data, blog_post=blog_post
        )
        db_session.add(blog_post_translation)

    for translation in translations:
        if translation["language"] != "en" and english_translation_data:
            for key in english_translation_data:
                if translation.get(key) is None:
                    translation[key] = english_translation_data[key]

            blog_post_translation = BlogPostTranslation(
                **translation, blog_post=blog_post
            )
            db_session.add(blog_post_translation)


def import_mempool():
    click.echo("Importing Mempool...", nl=False)
    blog_post_translations = {}
    blog_posts = {}
    directory_path = "content/mempool"

    for filename in sorted(os.listdir(directory_path)):
        slug, lang, _ = extract_data_from_filename(filename)
        if lang == "en":
            process_english_file(
                filename, directory_path, blog_posts, blog_post_translations
            )

    for filename in sorted(os.listdir(directory_path)):
        slug, lang, _ = extract_data_from_filename(filename)
        if lang != "en":
            process_other_language_file(
                filename, directory_path, blog_post_translations
            )

    for slug, translations in blog_post_translations.items():
        handle_translations_for_slug(slug, translations, blog_posts, db.session)

    db.session.commit()
    click.echo(DONE)
