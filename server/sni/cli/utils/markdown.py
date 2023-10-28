import collections
import os
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Type

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


IMPORT_MESSAGE = "Importing {content_type}..."
SUMMARY_MESSAGE = "{new_files} new, {updated_files} updated, {deleted_files} deleted"


class BaseImporter:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.files_in_db = {}
        self.actions = collections.Counter(new=0, updated=0, deleted=0, unchanged=0)

    @property
    def filenames(self):
        return sorted(os.listdir(self.directory_path))

    def run_import(self):
        click.echo(IMPORT_MESSAGE.format(content_type=self.content_type), nl=False)
        self.import_content()
        click.echo(DONE)
        click.echo(
            SUMMARY_MESSAGE.format(
                new_files=self.actions["new"],
                updated_files=self.actions["updated"],
                deleted_files=self.actions["deleted"],
            )
        )
        click.echo()

    def _populate_files_from_db(self):
        self.files_in_db = {
            content.file_metadata.filename: content
            for content in db.session.scalars(
                db.select(MarkdownContent).filter_by(content_type=self.content_key)
            ).all()
        }

    def _get_file_hash(self, filepath):
        return get_file_hash(filepath)

    def _needs_update(self, file_record, current_hash, current_timestamp):
        return (
            file_record.file_metadata.hash != current_hash
            or file_record.file_metadata.last_modified != current_timestamp
        )

    def _create_new_metadata(self, filepath, current_hash, current_timestamp):
        new_metadata = FileMetadata(
            filename=filepath, hash=current_hash, last_modified=current_timestamp
        )
        db.session.add(new_metadata)
        return new_metadata

    def _update_existing_metadata(self, file_record, current_hash, current_timestamp):
        current_metadata = file_record.file_metadata
        current_metadata.hash = current_hash
        current_metadata.last_modified = current_timestamp
        db.session.add(current_metadata)
        return current_metadata

    def _process_deleted_files(self):
        deleted_files_count = len(self.files_in_db)
        for deleted_file in self.files_in_db.values():
            db.session.delete(deleted_file)
        return deleted_files_count


class ContentImporter(BaseImporter):
    def import_content(self):
        self._populate_files_from_db()

        for filename in self.filenames:
            action = self._process_file(filename)
            self.actions[action] += 1

        self.actions["deleted"] = self._process_deleted_files()
        db.session.commit()

    def _process_file(self, filename):
        filepath = os.path.join(self.directory_path, filename)
        current_hash = self._get_file_hash(filepath)
        current_timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))

        file_record = self.files_in_db.pop(filepath, None)
        new_metadata = None

        if not file_record:
            new_metadata = self._create_new_metadata(
                filepath, current_hash, current_timestamp
            )
            action = "new"
        elif self._needs_update(file_record, current_hash, current_timestamp):
            new_metadata = self._update_existing_metadata(
                file_record, current_hash, current_timestamp
            )
            action = "updated"
        else:
            action = "unchanged"

        if new_metadata:
            slug, *_ = extract_data_from_filename(filename)
            self._process_and_add_file(new_metadata, slug)

        return action

    def _process_and_add_file(self, metadata, slug):
        validated_data, content = process_markdown_file(metadata.filename, self.schema)
        new_entry = self.model(
            **validated_data,
            slug=slug,
            content=content,
            file_metadata=metadata,
            content_type=self.content_key,
        )
        db.session.add(new_entry)


class TranslatedContentImporter(BaseImporter):
    def __init__(self, directory_path):
        super().__init__(directory_path)
        self.content_map = {}
        self.english_filenames = []
        self.non_english_filenames = []

    def import_content(self):
        self._populate_files_from_db()

        for filename in self.filenames:
            _, locale, _ = extract_data_from_filename(filename)
            if locale == "en":
                self.english_filenames.append(filename)
            else:
                self.non_english_filenames.append(filename)

        for filename in self.english_filenames:
            metadata = self._process_file(filename)
            if metadata:
                slug, _, _ = extract_data_from_filename(filename)
                self.process_and_add_canonical_file(metadata, slug)

        for filename in self.non_english_filenames:
            metadata = self._process_file(filename)
            if metadata:
                slug, locale, _ = extract_data_from_filename(filename)
                self.process_and_add_translated_file(metadata, slug, locale)

        self.actions["deleted"] = self._process_deleted_files()
        db.session.commit()

    def _process_file(self, filename):
        filepath = os.path.join(self.directory_path, filename)
        current_hash = get_file_hash(filepath)
        current_timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))

        file_record = self.files_in_db.pop(filepath, None)
        new_metadata = None

        if not file_record:
            self.actions["new"] += 1
            new_metadata = self._create_new_metadata(
                filepath, current_hash, current_timestamp
            )
        elif self._needs_update(file_record, current_hash, current_timestamp):
            self.actions["updated"] += 1
            new_metadata = self._update_existing_metadata(
                file_record, current_hash, current_timestamp
            )

        return new_metadata

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

        canonical_entry_data = self.process_canonical_additional_data(canonical_data)
        canonical_entry = self.canonical_model(**canonical_entry_data)
        db.session.add(canonical_entry)
        db.session.flush()

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
