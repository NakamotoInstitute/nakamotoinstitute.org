import collections
import os
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Type

import click
import yaml
from pydantic import BaseModel, ValidationError

from sni.cli.utils import DONE
from sni.config import Locales
from sni.extensions import db
from sni.shared.models import FileMetadata, MarkdownContent
from sni.utils.files import get_file_hash, split_filename


class BaseMarkdownImporter:
    def __init__(self):
        self.files_in_db = {}
        self.actions = collections.Counter(new=0, updated=0, deleted=0, unchanged=0)

    @property
    def filenames(self):
        return sorted(os.listdir(self.directory_path))

    def run_import(self):
        click.echo(f"Importing {self.content_type}...", nl=False)
        self.import_content()
        click.echo(DONE)
        click.echo(
            "{new_files} new, {updated_files} updated, {deleted_files} deleted".format(
                new_files=self.actions["new"],
                updated_files=self.actions["updated"],
                deleted_files=self.actions["deleted"],
            )
        )
        click.echo()

    def read_markdown_file(self, filepath: str) -> str:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()

    def parse_front_matter(self, filepath: str) -> Tuple[Optional[Dict[Any, Any]], str]:
        content = self.read_markdown_file(filepath)
        split_content = content.split("---\n")
        if len(split_content) < 3:
            return None, content
        front_matter_str = split_content[1]
        remaining_content = "---\n".join(split_content[2:]).strip()
        return yaml.safe_load(front_matter_str), remaining_content

    def validate_front_matter(
        self, front_matter: Dict[Any, Any], schema: Type[BaseModel]
    ) -> Optional[BaseModel]:
        try:
            return schema.parse_obj(front_matter)
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None

    def process_markdown_file(
        self, filepath: str, schema: Type[BaseModel]
    ) -> Tuple[Optional[Dict[Any, Any]], str]:
        raw_front_matter, remaining_content = self.parse_front_matter(filepath)

        if raw_front_matter:
            validated_front_matter = self.validate_front_matter(
                raw_front_matter, schema
            )
            if validated_front_matter:
                return validated_front_matter.dict(), remaining_content

        return None, remaining_content

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
        return file_record.file_metadata.hash != current_hash

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


class MarkdownImporter(BaseMarkdownImporter):
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
            slug, *_ = split_filename(filename)
            self._process_and_add_file(new_metadata, slug, action)

        return action

    def _process_and_add_file(self, metadata, slug, action):
        validated_data, content = self.process_markdown_file(
            metadata.filename, self.schema
        )

        if action == "updated":
            existing_entry = db.session.scalars(
                db.select(self.model).filter_by(file_metadata=metadata)
            ).first()
            if existing_entry:
                for key, value in validated_data.items():
                    setattr(existing_entry, key, value)
                existing_entry.slug = slug
                existing_entry.content = content
                existing_entry.file_metadata = metadata
                existing_entry.content_type = self.content_key
            else:
                raise ValueError(
                    f"No existing {self.model.__name__} found for updated metadata: {metadata.id}"  # noqa: E501
                )

        elif action == "new":
            new_entry = self.model(
                **validated_data,
                slug=slug,
                content=content,
                file_metadata=metadata,
                content_type=self.content_key,
            )
            db.session.add(new_entry)


class TranslatedMarkdownImporter(BaseMarkdownImporter):
    def __init__(self):
        super().__init__()
        self.content_map = {}
        (
            self.english_filenames,
            self.non_english_filenames,
        ) = self._categorize_filenames()

    def _categorize_filenames(self):
        english_filenames = []
        non_english_filenames = []

        for filename in self.filenames:
            _, locale, _ = split_filename(filename)
            if locale == "en":
                english_filenames.append(filename)
            else:
                non_english_filenames.append(filename)

        return english_filenames, non_english_filenames

    def import_content(self):
        self._populate_files_from_db()
        self._import_english_content()
        db.session.commit()
        self._populate_content_map_from_db()
        self._import_translated_content()
        self.actions["deleted"] = self._process_deleted_files()
        db.session.commit()

    def _import_english_content(self):
        for filename in self.english_filenames:
            action = self._process_file(filename)
            self.actions[action] += 1

    def _import_translated_content(self):
        for filename in self.non_english_filenames:
            action = self._process_file(filename, english=False)
            self.actions[action] += 1

    def _populate_content_map_from_db(self):
        all_canonical_entries = db.session.query(self.canonical_model).all()
        for entry in all_canonical_entries:
            english_translation = next(
                (t for t in entry.translations if t.locale == Locales.ENGLISH), None
            )
            self.content_map[english_translation.slug] = {
                "canonical": entry,
                "translation": english_translation,
            }

    def _process_file(self, filename, english=True):
        filepath = os.path.join(self.directory_path, filename)
        current_hash = get_file_hash(filepath)
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
            slug, locale, *_ = split_filename(filename)
            if english:
                self.process_and_add_canonical_file(new_metadata, slug, action)
            else:
                self.process_and_add_translated_file(new_metadata, slug, locale, action)

        return action

    def _process_canonical_file(self, filepath: str, canonical_schema, schema):
        front_matter_dict, content = self.parse_front_matter(filepath)
        canonical_data = self.validate_front_matter(front_matter_dict, canonical_schema)
        translation_data = self.validate_front_matter(front_matter_dict, schema)
        return canonical_data, translation_data, content

    def process_and_add_canonical_file(self, metadata, slug, action):
        (
            validated_canonical_data,
            validated_translation_data,
            content,
        ) = self._process_canonical_file(
            metadata.filename, self.canonical_schema, self.md_schema
        )

        canonical_data = validated_canonical_data.dict()
        translation_data = validated_translation_data.dict()

        if action == "updated":
            existing_translation_entry = db.session.scalars(
                db.select(self.translation_model).filter_by(file_metadata=metadata)
            ).first()
            if existing_translation_entry:
                existing_canonical_entry = getattr(
                    existing_translation_entry, self.content_key, None
                )
                translation_entry_data = self.process_translation_additional_data(
                    translation_data, existing_canonical_entry, metadata
                )
                for key, value in translation_data.items():
                    setattr(existing_translation_entry, key, value)
                existing_translation_entry.slug = slug
                existing_translation_entry.locale = "en"
                existing_translation_entry.content = content
                db.session.add(existing_translation_entry)

                existing_canonical_entry = getattr(
                    existing_translation_entry, self.content_key, None
                )
                if existing_canonical_entry:
                    canonical_entry_data = self.process_canonical_additional_data(
                        canonical_data
                    )
                    for key, value in canonical_data.items():
                        setattr(existing_canonical_entry, key, value)
                    db.session.add(existing_canonical_entry)

        elif action == "new":
            canonical_entry_data = self.process_canonical_additional_data(
                canonical_data
            )
            canonical_entry = self.canonical_model(**canonical_entry_data)
            db.session.add(canonical_entry)
            db.session.flush()

            translation_entry_data = self.process_translation_additional_data(
                translation_data, canonical_entry, metadata
            )
            translation_entry = self.translation_model(
                **translation_entry_data,
                slug=slug,
                locale=Locales.ENGLISH,
                content=content,
                **{self.content_key: canonical_entry},
            )
            db.session.add(translation_entry)

    def process_canonical_additional_data(self, canonical_data):
        return canonical_data

    def process_translation_additional_data(
        self, translation_data, canonical_entry, metadata
    ):
        return self._process_translation_metadata(translation_data, metadata)

    def process_and_add_translated_file(self, metadata, slug, locale, action):
        validated_translation_data, content = self.process_markdown_file(
            metadata.filename, self.translation_schema
        )
        translation_data = validated_translation_data

        canonical_entry = self.content_map.get(slug)
        if not canonical_entry:
            return

        translation_data["slug"] = translation_data.get("slug") or slug
        translation_entry_data = self.process_translation_for_translated_file(
            translation_data, canonical_entry, metadata
        )

        if action == "updated":
            existing_translation_entry = db.session.scalars(
                db.select(self.translation_model).filter_by(file_metadata=metadata)
            ).first()
            for key, value in translation_data.items():
                setattr(existing_translation_entry, key, value)
            existing_translation_entry.locale = locale
            existing_translation_entry.content = content
            db.session.add(existing_translation_entry)
        elif action == "new":
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
