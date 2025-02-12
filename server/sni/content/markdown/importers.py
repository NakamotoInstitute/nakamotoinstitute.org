import os
from abc import ABC, abstractmethod

from sqlalchemy import select

from sni.constants import Locales
from sni.database import SessionLocalSync
from sni.models import HTMLRenderableContent, MarkdownContent
from sni.utils.files import split_filename

from ..metadata import Actions, MetadataManager
from .file_processor import process_file


def select_schemas(schemas: dict, *keys: str) -> dict:
    return {k: schemas[k] for k in keys}


class BaseMarkdownImporter(ABC):
    content_type: str

    def __init__(self):
        self.files_in_db = {}
        self.db_session = SessionLocalSync()
        self.force = False
        self.metadata_manager = MetadataManager(self.db_session, force=self.force)
        self.schemas = self.get_schema_dict()

    @abstractmethod
    def get_schema_dict(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def import_content(self) -> None:
        pass

    @property
    def filenames(self):
        files = [
            f
            for f in os.listdir(self.directory_path)
            if os.path.isfile(os.path.join(self.directory_path, f))
        ]
        return sorted(files)

    def run_import(self, force: bool = False):
        self.force = force
        self.metadata_manager.force = force
        print(f"Importing {self.content_type}...", end="")
        try:
            self.import_content()
        finally:
            self.db_session.close()
        print("DONE")
        print(self.metadata_manager.get_action_summary())
        print()

    def _populate_files_from_db(self):
        self.files_in_db = {
            item.content.file_metadata.filename: item
            for item in self.db_session.scalars(select(self.model)).all()
            if os.path.isfile(item.content.file_metadata.filename)
        }

    def _process_deleted_files(self):
        deleted_files_count = len(self.files_in_db)
        for deleted_file in self.files_in_db.values():
            self.db_session.delete(deleted_file)
            self.metadata_manager.record_action(Actions.DELETED)
        return deleted_files_count


class MarkdownImporter(BaseMarkdownImporter):
    def get_schema_dict(self):
        return {"canonical": self.schema}

    def import_content(self):
        self._populate_files_from_db()

        for filename in self.filenames:
            self._process_file(filename)

        self._process_deleted_files()
        self.db_session.commit()

    def _process_file(self, filename):
        filepath = os.path.join(self.directory_path, filename)
        existing_file = self.files_in_db.pop(filepath, None)
        old_metadata = existing_file.content.file_metadata if existing_file else None
        action, new_metadata = self.metadata_manager.process_file(
            filepath, old_metadata
        )

        if new_metadata:
            slug, *_ = split_filename(filename)
            self._process_and_add_file(new_metadata, slug, action)

        self.metadata_manager.record_action(action)

    def _process_and_add_file(self, metadata, slug, action):
        results, html_content, file_content = process_file(
            metadata.filename, self.schemas
        )
        canonical_data = results["canonical"].data

        if action == Actions.UPDATED:
            existing_entry = self.db_session.scalars(
                select(self.model)
                .join(self.model.content)
                .filter(HTMLRenderableContent.file_metadata == metadata)
            ).first()
            if existing_entry:
                existing_entry.content.file_content = file_content
                existing_entry.content.html_content = html_content
                existing_entry.content.file_metadata = metadata
                canonical_data = self.process_canonical_additional_data(canonical_data)
                for key, value in canonical_data.items():
                    setattr(existing_entry, key, value)
                existing_entry.slug = slug
            else:
                raise ValueError(
                    f"No existing {self.model.__name__} found for updated metadata: {metadata.id}"  # noqa: E501
                )

        elif action == Actions.NEW:
            canonical_data = self.process_canonical_additional_data(canonical_data)
            new_content = MarkdownContent(
                file_content=file_content,
                html_content=html_content,
                file_metadata=metadata,
            )
            self.db_session.add(new_content)
            new_entry = self.model(
                **canonical_data,
                slug=slug,
                content=new_content,
            )
            self.db_session.add(new_entry)

    def process_canonical_additional_data(self, canonical_data):
        return canonical_data


class TranslatedMarkdownImporter(BaseMarkdownImporter):
    def __init__(self):
        super().__init__()
        self.content_map = {}
        (
            self.english_filenames,
            self.non_english_filenames,
        ) = self._categorize_filenames()

    def get_schema_dict(self):
        return {
            "canonical": self.canonical_schema,
            "translation": self.translation_schema,
        }

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

    def _populate_files_from_db(self):
        self.files_in_db = {
            item.content.file_metadata.filename: item
            for item in self.db_session.scalars(select(self.translation_model)).all()
            if os.path.isfile(item.content.file_metadata.filename)
        }

    def import_content(self):
        self._populate_files_from_db()
        self._import_english_content()
        self.db_session.commit()
        self._populate_content_map_from_db()
        self._import_translated_content()
        self._process_deleted_files()
        self.db_session.commit()

    def _import_english_content(self):
        for filename in self.english_filenames:
            self._process_file(filename)

    def _import_translated_content(self):
        for filename in self.non_english_filenames:
            self._process_file(filename, english=False)

    def _populate_content_map_from_db(self):
        all_canonical_entries = self.db_session.query(self.canonical_model).all()
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
        existing_file = self.files_in_db.pop(filepath, None)
        old_metadata = existing_file.content.file_metadata if existing_file else None
        action, new_metadata = self.metadata_manager.process_file(
            filepath, old_metadata
        )

        if new_metadata:
            slug, locale, *_ = split_filename(filename)
            if english:
                self.process_and_add_canonical_file(new_metadata, slug, action)
            else:
                self.process_and_add_translated_file(new_metadata, slug, locale, action)

        self.metadata_manager.record_action(action)

    def process_and_add_canonical_file(self, metadata, slug, action):
        results, html_content, file_content = process_file(
            metadata.filename, select_schemas(self.schemas, "canonical", "translation")
        )

        canonical_data = results["canonical"].data
        translation_data = results["translation"].data

        if action == Actions.UPDATED:
            existing_translation_entry = self.db_session.scalars(
                select(self.translation_model)
                .join(self.translation_model.content)
                .filter(HTMLRenderableContent.file_metadata == metadata)
            ).first()
            if existing_translation_entry:
                existing_canonical_entry = getattr(
                    existing_translation_entry, self.content_key, None
                )
                translation_entry_data = self.process_translation_additional_data(
                    translation_data, existing_canonical_entry, metadata
                )
                for key, value in translation_entry_data.items():
                    setattr(existing_translation_entry, key, value)
                existing_translation_entry.slug = slug
                existing_translation_entry.locale = Locales.ENGLISH
                existing_translation_entry.content.file_content = file_content
                existing_translation_entry.content.html_content = html_content
                self.db_session.add(existing_translation_entry)

                existing_canonical_entry = getattr(
                    existing_translation_entry, self.content_key, None
                )
                if existing_canonical_entry:
                    canonical_entry_data = self.process_canonical_additional_data(
                        canonical_data
                    )
                    for key, value in canonical_data.items():
                        setattr(existing_canonical_entry, key, value)
                    self.db_session.add(existing_canonical_entry)

        elif action == Actions.NEW:
            canonical_entry_data = self.process_canonical_additional_data(
                canonical_data
            )
            canonical_entry = self.canonical_model(**canonical_entry_data, slug=slug)
            self.db_session.add(canonical_entry)
            self.db_session.flush()

            translation_entry_data = self.process_translation_additional_data(
                translation_data, canonical_entry, metadata
            )
            translation_entry_data.pop("slug", None)

            new_content = MarkdownContent(
                file_content=file_content,
                html_content=html_content,
                file_metadata=metadata,
            )
            self.db_session.add(new_content)
            translation_entry = self.translation_model(
                **translation_entry_data,
                slug=slug,
                locale=Locales.ENGLISH,
                content=new_content,
                **{self.content_key: canonical_entry},
            )
            self.db_session.add(translation_entry)

    def process_canonical_additional_data(self, canonical_data):
        return canonical_data

    def process_translation_additional_data(
        self, translation_data, canonical_entry, metadata
    ):
        return self._process_translation_metadata(translation_data, metadata)

    def process_and_add_translated_file(self, metadata, slug, locale, action):
        results, html_content, file_content = process_file(
            metadata.filename, select_schemas(self.schemas, "translation")
        )
        translation_data = results["translation"].data

        canonical_entry = self.content_map.get(slug)
        if not canonical_entry:
            return

        translation_data["slug"] = translation_data.get("slug") or slug
        translation_entry_data = self.process_translation_for_translated_file(
            translation_data, canonical_entry, metadata
        )

        if action == Actions.UPDATED:
            existing_translation_entry = self.db_session.scalars(
                select(self.translation_model)
                .join(self.translation_model.content)
                .filter(HTMLRenderableContent.file_metadata == metadata)
            ).first()
            for key, value in translation_entry_data.items():
                setattr(existing_translation_entry, key, value)
            existing_translation_entry.locale = locale
            existing_translation_entry.content.file_content = file_content
            existing_translation_entry.content.html_content = html_content
            existing_translation_entry.content.file_metadata = metadata
            self.db_session.add(existing_translation_entry)
        elif action == Actions.NEW:
            new_content = MarkdownContent(
                file_content=file_content,
                html_content=html_content,
                file_metadata=metadata,
            )
            self.db_session.add(new_content)
            translation_entry = self.translation_model(
                **translation_entry_data,
                locale=locale,
                content=new_content,
                **{self.content_key: canonical_entry["canonical"]},
            )
            self.db_session.add(translation_entry)

    def process_translation_for_translated_file(
        self, translation_data, canonical_entry, metadata
    ):
        return self._process_translation_metadata(translation_data, metadata)

    def _process_translation_metadata(self, translation_data, metadata):
        return translation_data


class MarkdownDirectoryImporter(MarkdownImporter):
    def get_schema_dict(self):
        return {
            "manifest": self.manifest_schema,
            "canonical": self.canonical_schema,
            "translation": self.translation_schema,
            "node_content": self.node_content_schema,
        }

    @property
    def filenames(self):
        dirs = [
            d
            for d in os.listdir(self.directory_path)
            if os.path.isdir(os.path.join(self.directory_path, d))
        ]
        return sorted(dirs)

    def _populate_files_from_db(self):
        self.files_in_db = {
            item.content.file_metadata.filename: item
            for item in self.db_session.scalars(select(self.translation_model)).all()
            if os.path.isdir(item.content.file_metadata.filename)
        }

    def import_content(self):
        self._populate_files_from_db()

        for directory in self.filenames:
            self._process_directory(directory)

        self._process_deleted_files()
        self.db_session.commit()

    def _process_directory(self, directory):
        dir_path = os.path.join(self.directory_path, directory)
        existing_file = self.files_in_db.pop(dir_path, None)
        action, new_metadata = self.metadata_manager.process_file(
            dir_path, existing_file.content.file_metadata if existing_file else None
        )

        if new_metadata:
            self._process_and_add_directory(new_metadata, dir_path, directory, action)

        self.metadata_manager.record_action(action)

    def _process_and_add_directory(self, metadata, directory, slug, action):
        manifest_file = os.path.join(directory, "manifest.md")
        content_dir = os.path.join(directory, "content")

        if os.path.isfile(manifest_file) and os.path.isdir(content_dir):
            results, html_content, file_content = process_file(
                manifest_file,
                select_schemas(self.schemas, "manifest", "canonical", "translation"),
            )
            # We want to check against the validated data model when inserting nodes,
            # not the raw data
            manifest_schema_data = results["manifest"].model
            canonical_data = results["canonical"].data
            translation_data = results["translation"].data

            translation_entry = None

            if action == Actions.UPDATED:
                existing_translation_entry = self.db_session.scalars(
                    select(self.translation_model)
                    .join(self.translation_model.content)
                    .filter(HTMLRenderableContent.file_metadata == metadata)
                ).first()
                if existing_translation_entry:
                    existing_canonical_entry = getattr(
                        existing_translation_entry, self.content_key, None
                    )

                    self._delete_existing_nodes(existing_translation_entry.id)

                    translation_entry_data = self.process_translation_additional_data(
                        translation_data, existing_canonical_entry, metadata
                    )

                    for key, value in translation_entry_data.items():
                        setattr(existing_translation_entry, key, value)

                    existing_translation_entry.slug = slug
                    existing_translation_entry.locale = Locales.ENGLISH
                    existing_translation_entry.content.file_content = file_content
                    existing_translation_entry.content.html_content = html_content
                    self.db_session.add(existing_translation_entry)

                    existing_canonical_entry = getattr(
                        existing_translation_entry, self.content_key, None
                    )

                    if existing_canonical_entry:
                        canonical_entry_data = self.process_canonical_additional_data(
                            canonical_data
                        )
                        for key, value in canonical_data.items():
                            setattr(existing_canonical_entry, key, value)
                        self.db_session.add(existing_canonical_entry)
                    translation_entry = existing_translation_entry

            elif action == Actions.NEW:
                canonical_entry_data = self.process_canonical_additional_data(
                    canonical_data
                )
                canonical_entry = self.canonical_model(
                    **canonical_entry_data, slug=slug
                )
                self.db_session.add(canonical_entry)
                self.db_session.flush()

                translation_entry_data = self.process_translation_additional_data(
                    translation_data, canonical_entry, metadata
                )
                translation_entry_data.pop("slug")

                new_content = MarkdownContent(
                    file_content=file_content,
                    html_content=html_content,
                    file_metadata=metadata,
                )
                self.db_session.add(new_content)
                translation_entry = self.translation_model(
                    **translation_entry_data,
                    slug=slug,
                    locale=Locales.ENGLISH,
                    content=new_content,
                    **{self.content_key: canonical_entry},
                )
                self.db_session.add(translation_entry)
                self.db_session.flush()

            if translation_entry:
                self._insert_nodes(
                    manifest_schema_data.nodes,
                    None,
                    translation_entry.id,
                    1,
                    content_dir,
                )

    def process_canonical_additional_data(self, canonical_data):
        return canonical_data

    def process_translation_additional_data(
        self, translation_data, canonical_entry, metadata
    ):
        return self._process_translation_metadata(translation_data, metadata)

    def _process_translation_metadata(self, translation_data, metadata):
        return translation_data

    def _delete_existing_nodes(self, content_reference_id):
        nodes_to_delete = self.db_session.scalars(
            select(self.node_model).filter_by(
                **{self.content_reference_id: content_reference_id}
            )
        ).all()

        for node in nodes_to_delete:
            self.db_session.delete(node)

        self.db_session.commit()

    def _insert_nodes(
        self, node_data, parent_id, content_reference_id, order, content_dir
    ):
        if isinstance(node_data, list):
            for idx, child in enumerate(node_data, start=1):
                self._insert_nodes(
                    child, parent_id, content_reference_id, idx, content_dir
                )
        elif isinstance(node_data, str):
            node = self._insert_node(
                node_data, order, parent_id, content_reference_id, content_dir
            )
            return node.id
        elif isinstance(node_data, self.node_schema):
            node = self._insert_node(
                node_data.slug, order, parent_id, content_reference_id, content_dir
            )
            node_id = node.id
            for idx, child in enumerate(node_data.children, start=1):
                self._insert_nodes(
                    child, node_id, content_reference_id, idx, content_dir
                )
            return node_id

    def _insert_node(self, slug, order, parent_id, content_reference_id, content_dir):
        md_file = os.path.join(content_dir, f"{slug}.md")
        results, html_content, file_content = process_file(
            md_file, select_schemas(self.schemas, "node_content")
        )
        node_data = results["node_content"].data

        node = self.node_model(
            slug=slug,
            **node_data,
            order=order,
            html_content=html_content,
            file_content=file_content,
            parent_id=parent_id,
            **{self.content_reference_id: content_reference_id},
        )
        self.db_session.add(node)
        self.db_session.commit()

        return node
