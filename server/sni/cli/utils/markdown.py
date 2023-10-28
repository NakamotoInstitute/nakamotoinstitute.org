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
from sni.shared.models import FileMetadata, MarkdownContent
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
        self.files_in_db = {}
        self.new_files = 0
        self.updated_files = 0
        self.deleted_files = 0

    def _identify_files(self):
        self._populate_files_from_db()

        for filename in sorted(os.listdir(self.directory_path)):
            _, locale, _ = extract_data_from_filename(filename)
            if locale == "en":
                self.english_filenames.append(filename)
            else:
                self.non_english_filenames.append(filename)

    def _populate_files_from_db(self):
        self.files_in_db = {
            content.file_metadata.filename: content
            for content in db.session.scalars(
                db.select(MarkdownContent).filter_by(content_type=self.content_key)
            ).all()
        }

    def process_and_add_canonical_file(self, metadata, slug):
        (
            validated_canonical_data,
            validated_translation_data,
            content,
        ) = process_canonical_file(
            metadata.filename, self.canonical_schema, self.md_schema
        )

        canonical_data = validated_canonical_data.dict()
        translation_data = validated_translation_data.dict()

        # Hook: Process additional data for canonical entry
        canonical_entry_data = self.process_canonical_additional_data(canonical_data)
        canonical_entry = self.canonical_model(**canonical_entry_data)
        db.session.add(canonical_entry)
        db.session.flush()

        # Hook: Process additional data for translation entry
        translation_entry_data = self.process_translation_additional_data(
            translation_data, canonical_entry, metadata
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
        self, translation_data, canonical_entry, metadata
    ):
        return self._process_translation_metadata(translation_data, metadata)

    def process_and_add_translated_file(self, metadata, slug, locale):
        validated_translation_data, content = process_translated_file(
            metadata.filename, self.translation_schema
        )
        translation_data = validated_translation_data.dict()

        canonical_entry = self.content_map.get(slug)
        if not canonical_entry:
            return

        translation_data["slug"] = translation_data.get("slug") or slug
        translation_entry_data = self.process_translation_for_translated_file(
            translation_data, canonical_entry, metadata
        )

        translation_entry = self.translation_model(
            **translation_entry_data,
            locale=locale,
            content=content,
            **{self.content_key: canonical_entry["canonical"]},
        )
        db.session.add(translation_entry)

    def process_translation_for_translated_file(
        self, translation_data, canonical_entry, metadata
    ):
        return self._process_translation_metadata(translation_data, metadata)

    def _process_translation_metadata(self, translation_data, metadata):
        translation_data["file_metadata"] = metadata
        translation_data["content_type"] = self.content_key
        return translation_data

    def _process_file(self, filename):
        filepath = os.path.join(self.directory_path, filename)
        current_hash = get_file_hash(filepath)
        current_timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))

        file_record = self.files_in_db.pop(filepath, None)
        new_metadata = None

        if not file_record:
            self.new_files += 1
            new_metadata = self._create_new_metadata(
                filepath, current_hash, current_timestamp
            )
        elif (
            file_record.hash != current_hash
            or file_record.last_modified_timestamp != current_timestamp
        ):
            self.updated_files += 1
            new_metadata = self._update_existing_metadata(
                file_record, current_hash, current_timestamp
            )

        return new_metadata, filepath

    @staticmethod
    def _create_new_metadata(filepath, current_hash, current_timestamp):
        new_metadata = FileMetadata(
            filename=filepath, hash=current_hash, last_modified=current_timestamp
        )
        db.session.add(new_metadata)
        return new_metadata

    def _update_existing_metadata(self, file_record, current_hash, current_timestamp):
        current_metadata = file_record.file_metadata
        if (
            current_metadata.hash != current_hash
            or current_metadata.last_modified != current_timestamp
        ):
            current_metadata.hash = current_hash
            current_metadata.last_modified = current_timestamp
            db.session.add(current_metadata)
        return current_metadata

    def import_content(self):
        self._identify_files()

        for filename in self.english_filenames:
            metadata, _ = self._process_file(filename)
            if metadata:
                slug, _, _ = extract_data_from_filename(filename)
                self.process_and_add_canonical_file(metadata, slug)

        for filename in self.non_english_filenames:
            metadata, filepath = self._process_file(filename)
            if metadata:
                slug, locale, _ = extract_data_from_filename(filename)
                self.process_and_add_translated_file(metadata, slug, locale)

        self.deleted_files = len(self.files_in_db)
        for deleted_file in self.files_in_db.values():
            db.session.delete(deleted_file)

        db.session.commit()

    def run_import(self):
        click.echo(f"Importing {self.content_type}...", nl=False)
        self.import_content()
        click.echo(
            f"{self.new_files} new, {self.updated_files} updated, {self.deleted_files} deleted"  # noqa E501
        )
        click.echo(
            DONE,
        )
