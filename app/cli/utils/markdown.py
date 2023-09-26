import os
from typing import Any, Dict, List, Optional, Tuple, Type

import click
import yaml
from pydantic import BaseModel, ValidationError

from app import db
from app.cli.utils import DONE, get
from app.models import Author


def read_markdown_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def parse_front_matter(content: str) -> Tuple[Optional[Dict[Any, Any]], str]:
    split_content = content.split("---\n")
    if len(split_content) < 3:
        return None, content
    front_matter_str = split_content[1]
    remaining_content = "---\n".join(split_content[2:]).strip()
    return yaml.safe_load(front_matter_str), remaining_content


def validate_front_matter(
    front_matter: Dict[Any, Any], schema: Type[BaseModel]
) -> Optional[BaseModel]:
    try:
        return schema.parse_obj(front_matter)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None


def process_markdown_file(
    filepath: str, schema: Type[BaseModel]
) -> Tuple[Optional[Dict[Any, Any]], str]:
    content = read_markdown_file(filepath)
    raw_front_matter, remaining_content = parse_front_matter(content)

    if raw_front_matter:
        validated_front_matter = validate_front_matter(raw_front_matter, schema)
        if validated_front_matter:
            return validated_front_matter.dict(), remaining_content
        else:
            return None, remaining_content

    return None, content


def load_all_markdown_files(
    directory_path: str, schema: Type[BaseModel]
) -> List[Dict[str, Any]]:
    files_data: List[Dict[str, Any]] = []

    for filename in sorted(os.listdir(directory_path)):
        if filename.endswith(".md"):
            filepath = os.path.join(directory_path, filename)
            front_matter_dict, remaining_content = process_markdown_file(
                filepath, schema
            )

            if front_matter_dict is not None:
                file_data = dict(
                    **front_matter_dict,
                    slug=filename.split(".")[0],
                    content=remaining_content,
                )
                files_data.append(file_data)

    return files_data


def extract_data_from_filename(filename):
    return filename.split(".")


def _setup_common_data(slug, lang, extension, directory_path, schema):
    filepath = os.path.join(directory_path, f"{slug}.{lang}.{extension}")
    content = read_markdown_file(filepath)
    raw_front_matter, remaining_content = parse_front_matter(content)

    if raw_front_matter is None:
        return None, None

    front_matter = validate_front_matter(raw_front_matter, schema)
    if front_matter is None:
        return None, None

    return front_matter.dict(), remaining_content


def _load_common_data(slug, lang, extension, directory_path, schema):
    filepath = os.path.join(directory_path, f"{slug}.{lang}.{extension}")
    front_matter_dict, remaining_content = process_markdown_file(filepath, schema)

    if front_matter_dict:
        return front_matter_dict, remaining_content
    return None, None


def process_primary_language_file(
    filename, directory_path, items, item_translations, primary_schema
):
    slug, lang, extension = extract_data_from_filename(filename)
    front_matter_dict, remaining_content = _load_common_data(
        slug, lang, extension, directory_path, primary_schema
    )

    if not front_matter_dict:
        return

    keys_to_move = ["title", "excerpt", "image_alt"]
    translation_data = {"language": lang, "slug": slug, "content": remaining_content}
    for key in keys_to_move:
        translation_data[key] = front_matter_dict.pop(key, None)

    items[slug] = front_matter_dict
    item_translations[slug] = [translation_data]


def process_secondary_language_file(
    filename, directory_path, item_translations, secondary_schema
):
    slug, lang, extension = extract_data_from_filename(filename)
    front_matter_dict, remaining_content = _load_common_data(
        slug, lang, extension, directory_path, secondary_schema
    )

    if not front_matter_dict:
        return

    translation_data = {
        "language": lang,
        "slug": slug,
        "content": remaining_content,
        **front_matter_dict,
    }

    primary_language_data = next(
        (item for item in item_translations[slug] if item["language"] == "en"), {}
    )
    translation_data = {**primary_language_data, **translation_data}

    item_translations.setdefault(slug, []).append(translation_data)


def handle_translations(
    slug, translations, items, db_session, model, translation_model, relationship_key
):
    item_data = items.get(slug, {})

    if "authors" in item_data:
        item_data["authors"] = [
            get(Author, slug=author) for author in item_data["authors"]
        ]

    item_instance = model(**item_data)
    db_session.add(item_instance)

    primary_language_data = next(
        (item for item in translations if item["language"] == "en"), None
    )

    if primary_language_data:
        translation_instance = translation_model(
            **primary_language_data, **{relationship_key: item_instance}
        )
        db_session.add(translation_instance)

    for translation in translations:
        if translation["language"] != "en" and primary_language_data:
            for key in primary_language_data:
                if translation.get(key) is None:
                    translation[key] = primary_language_data[key]

            translation_instance = translation_model(
                **translation, **{relationship_key: item_instance}
            )
            db_session.add(translation_instance)


def import_content(
    directory_path,
    primary_schema,
    secondary_schema,
    model,
    translation_model,
    relationship_key,
):
    click.echo(f"Importing content from {directory_path}...", nl=False)
    item_translations = {}
    items = {}

    for filename in sorted(os.listdir(directory_path)):
        slug, lang, _ = extract_data_from_filename(filename)
        if lang == "en":
            process_primary_language_file(
                filename, directory_path, items, item_translations, primary_schema
            )

    for filename in sorted(os.listdir(directory_path)):
        slug, lang, _ = extract_data_from_filename(filename)
        if lang != "en":
            process_secondary_language_file(
                filename, directory_path, item_translations, secondary_schema
            )

    for slug, translations in item_translations.items():
        handle_translations(
            slug,
            translations,
            items,
            db.session,
            model,
            translation_model,
            relationship_key,
        )

    db.session.commit()
    click.echo(DONE)
