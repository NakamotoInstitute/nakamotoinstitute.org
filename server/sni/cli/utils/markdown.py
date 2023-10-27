import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Type

import click
import yaml
from pydantic import BaseModel, ValidationError

from sni.cli.utils import (
    DONE,
)
from sni.extensions import db
from sni.shared.models import FileMetadata
from sni.utils.files import get_file_hash


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


def process_common(filepath: str):
    file_content = read_markdown_file(filepath)
    front_matter_dict, content = parse_front_matter(file_content)
    return front_matter_dict, content


def validate_front_matter_data(front_matter_dict: dict, schema):
    return schema(**front_matter_dict)


def process_canonical_file(filepath: str, canonical_schema, schema):
    front_matter_dict, content = process_common(filepath)
    canonical_data = validate_front_matter_data(front_matter_dict, canonical_schema)
    translation_data = validate_front_matter_data(front_matter_dict, schema)
    return canonical_data, translation_data, content


def process_translated_file(filepath: str, translated_schema):
    front_matter_dict, content = process_common(filepath)
    translation_data = validate_front_matter_data(front_matter_dict, translated_schema)
    return translation_data, content


class ContentImporter:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.content_map = {}
        self.english_filenames = []
        self.non_english_filenames = []

    def _identify_files(self):
        for filename in sorted(os.listdir(self.directory_path)):
            _, locale, _ = extract_data_from_filename(filename)
            if locale == "en":
                self.english_filenames.append(filename)
            else:
                self.non_english_filenames.append(filename)

    def process_and_add_canonical_file(self, filepath, slug):
        (
            validated_canonical_data,
            validated_translation_data,
            content,
        ) = process_canonical_file(filepath, self.canonical_schema, self.md_schema)

        canonical_data = validated_canonical_data.dict()
        translation_data = validated_translation_data.dict()

        # Hook: Process additional data for canonical entry
        canonical_entry_data = self.process_canonical_additional_data(canonical_data)
        canonical_entry = self.canonical_model(**canonical_entry_data)
        db.session.add(canonical_entry)
        db.session.flush()

        # Hook: Process additional data for translation entry
        translation_entry_data = self.process_translation_additional_data(
            translation_data, canonical_entry, filepath
        )
        translation_entry = self.translation_model(
            **translation_entry_data,
            slug=slug,
            locale="en",
            content=content,
            **{self.content_key: canonical_entry},
        )
        db.session.add(translation_entry)

        self.content_map[slug] = {
            "canonical": canonical_entry,
            "translation": translation_entry,
        }

    # Hook method placeholders in base class (can be overridden in derived classes)
    def process_canonical_additional_data(self, canonical_data):
        return canonical_data

    def process_translation_additional_data(
        self, translation_data, canonical_entry, filepath
    ):
        return self._process_file_metadata(translation_data, filepath)

    def process_and_add_translated_file(self, filepath, slug, locale):
        validated_translation_data, content = process_translated_file(
            filepath, self.translation_schema
        )
        translation_data = validated_translation_data.dict()

        canonical_entry = self.content_map.get(slug)
        if not canonical_entry:
            return

        translation_data["slug"] = translation_data.get("slug") or slug
        translation_entry_data = self.process_translation_for_translated_file(
            translation_data, canonical_entry, filepath
        )

        translation_entry = self.translation_model(
            **translation_entry_data,
            locale=locale,
            content=content,
            **{self.content_key: canonical_entry["canonical"]},
        )
        db.session.add(translation_entry)

    def process_translation_for_translated_file(
        self, translation_data, canonical_entry, filepath
    ):
        return self._process_file_metadata(translation_data, filepath)

    def _process_file_metadata(self, translation_data, filepath):
        file_hash = get_file_hash(filepath)
        file_metadata = FileMetadata(
            filename=filepath, hash=file_hash, last_modified=datetime.now()
        )
        translation_data["file_metadata"] = file_metadata
        translation_data["content_type"] = self.content_key
        return translation_data

    def import_content(self):
        self._identify_files()

        for filename in self.english_filenames:
            filepath = os.path.join(self.directory_path, filename)
            slug, _, _ = extract_data_from_filename(filename)
            self.process_and_add_canonical_file(filepath, slug)

        for filename in self.non_english_filenames:
            filepath = os.path.join(self.directory_path, filename)
            slug, locale, _ = extract_data_from_filename(filename)
            self.process_and_add_translated_file(filepath, slug, locale)

        db.session.commit()

    def run_import(self):
        click.echo(f"Importing {self.content_type}...", nl=False)
        self.import_content()
        click.echo(DONE)
